const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

export const getProjects = async (minViews = 100) => {
  const response = await fetch(`${API_BASE_URL}/projects?minViews=${minViews}`);
  
  if (!response.ok) {
    throw new Error('Не удалось загрузить проекты');
  }
  
  return response.json();
};

export const getProjectById = async (id) => {
  const response = await fetch(`${API_BASE_URL}/projects/${id}`);
  
  if (!response.ok) {
    throw new Error('Не удалось загрузить проект');
  }
  
  return response.json();
};

export const searchProjects = async (searchTerm) => {
  const response = await fetch(`${API_BASE_URL}/projects/search?q=${encodeURIComponent(searchTerm)}`);
  
  if (!response.ok) {
    throw new Error('Ошибка поиска');
  }
  
  return response.json();
};