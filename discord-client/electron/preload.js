const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('desktop', {
  version: process.versions,
  controls: {
    minimize: () => ipcRenderer.send('window-control', 'minimize'),
    maximize: () => ipcRenderer.send('window-control', 'maximize'),
    close: () => ipcRenderer.send('window-control', 'close'),
    getState: () => ipcRenderer.invoke('window-query-state'),
  },
  onWindowStateChange: (callback) => {
    if (typeof callback !== 'function') {
      return () => {};
    }
    const handler = (_event, state) => callback(state);
    ipcRenderer.on('window-state', handler);
    return () => ipcRenderer.removeListener('window-state', handler);
  },
});
