
import {jwtDecode} from 'jwt-decode'

export const getToken = () => {
  return localStorage.getItem('authToken');
};

export const isTokenExpired = (token: string): boolean => {
  try {
    const decoded: any = jwtDecode(token);
    const expirationDate = decoded.exp * 1000; // Токен хранит дату истечения в секундах, преобразуем в миллисекунды
    const currentDate = new Date().getTime();
    return currentDate > expirationDate; // Возвращаем true, если токен истёк
  } catch (e) {
    console.error('Не удалось декодировать токен:', e);
    return true; // Если токен повреждён или недействителен
  }
};

export const isAuthenticated = (token:string): boolean => {
  
  if (token && !isTokenExpired(token)) {
    return true;
  }
  return false;
};
