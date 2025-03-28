import {jwtDecode} from 'jwt-decode'

export const getToken = () => {
  return localStorage.getItem('authToken');
};

export const isTokenExpired = (token: string): boolean => {
  try {
    const decoded: any = jwtDecode(token);
    const expirationDate = decoded.exp * 1000; 
    const currentDate = new Date().getTime();
    return currentDate > expirationDate; 
  } catch (e) {
    console.error('Не удалось декодировать токен:', e);
    return true; 
  }
};

export const isAuthenticated = (token:string): boolean => {
  
  if (token && !isTokenExpired(token)) {
    return true;
  }
  return false;
};

export const logout = async (router: any) => {
  try {
    await fetch('http://127.0.0.1:8000/admin/logout', {
      method: 'POST',
      headers: {
        'Authorization': `${getToken()}`
      }
    });
    localStorage.removeItem('authToken');
    router.push('/auth');
  } catch (error) {
    console.error('Ошибка при выходе:', error);
  }
};
