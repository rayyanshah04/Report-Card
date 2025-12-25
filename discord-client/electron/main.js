import { app, BrowserWindow, ipcMain } from 'electron';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawn } from 'node:child_process';
import fs from 'node:fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let pythonServer = null;
let mainWindow = null;

const isDev = process.env.VITE_DEV_SERVER_URL;

const ROOT_DIR = path.resolve(__dirname, '..', '..');
const PYTHON_ENTRY = path.join(ROOT_DIR, 'backend', 'app.py');
const BACKEND_EXE = path.join(process.resourcesPath, 'backend', 'report-backend.exe');
const SHOULD_START_BACKEND = process.env.FAIZAN_START_BACKEND !== '0';

function startPythonServer() {
  if (!SHOULD_START_BACKEND) return;
  if (pythonServer) return;
  const env = {
    ...process.env,
    PYTHONPATH: `${process.env.PYTHONPATH ? `${process.env.PYTHONPATH}${path.delimiter}` : ''}${ROOT_DIR}`,
    FAIZAN_BASE_DIR: app.isPackaged ? process.resourcesPath : ROOT_DIR,
  };
  if (app.isPackaged && fs.existsSync(BACKEND_EXE)) {
    pythonServer = spawn(BACKEND_EXE, [], { stdio: 'inherit', shell: false, env });
  } else {
    pythonServer = spawn('python', [PYTHON_ENTRY], {
      cwd: ROOT_DIR,
      stdio: 'inherit',
      shell: false,
      env,
    });
  }
  pythonServer.on('close', () => {
    pythonServer = null;
  });
}

const broadcastWindowState = () => {
  if (!mainWindow) return;
  const state = mainWindow.isMaximized() ? 'maximized' : 'normal';
  mainWindow.webContents.send('window-state', state);
};

async function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1440,
    height: 900,
    minWidth: 1200,
    minHeight: 720,
    backgroundColor: '#1f2128',
    frame: false,
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'hidden',
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    },
    show: false,
  });

  mainWindow.setMenuBarVisibility(false);

  mainWindow.once('ready-to-show', () => {
    if (!mainWindow) {
      return;
    }
    mainWindow.maximize();
    mainWindow.show();
    broadcastWindowState();
  });

  mainWindow.on('maximize', broadcastWindowState);
  mainWindow.on('unmaximize', broadcastWindowState);
  mainWindow.on('enter-full-screen', () => mainWindow?.webContents.send('window-state', 'maximized'));
  mainWindow.on('leave-full-screen', broadcastWindowState);

  if (isDev) {
    await mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
    mainWindow.webContents.openDevTools({ mode: 'detach' });
  } else {
    const indexHtml = path.join(app.getAppPath(), 'dist', 'index.html');
    await mainWindow.loadFile(indexHtml);
  }
}

ipcMain.on('window-control', (_event, action) => {
  if (!mainWindow) return;
  switch (action) {
    case 'minimize':
      mainWindow.minimize();
      break;
    case 'maximize':
      if (mainWindow.isMaximized()) {
        mainWindow.unmaximize();
      } else {
        mainWindow.maximize();
      }
      break;
    case 'close':
      mainWindow.close();
      break;
    default:
      break;
  }
  setTimeout(broadcastWindowState, 50);
});

ipcMain.handle('window-query-state', () => {
  if (!mainWindow) return 'normal';
  return mainWindow.isMaximized() ? 'maximized' : 'normal';
});

app.whenReady().then(() => {
  startPythonServer();
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  if (pythonServer) {
    pythonServer.kill();
  }
});
