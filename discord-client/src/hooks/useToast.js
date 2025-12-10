import useToastStore from '../store/toastStore';

const useToast = () => {
  const pushToast = useToastStore((state) => state.pushToast);
  return pushToast;
};

export default useToast;
