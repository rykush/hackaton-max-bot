const API_BASE_URL = import.meta.env.BASE_URL + 'projects.json';

let cachedProjects = null;

const loadAllProjects = async () => {
  if (cachedProjects) {
    return cachedProjects;
  }

  try {
    console.log('Загрузка проектов из:', API_BASE_URL);
    const response = await fetch(API_BASE_URL);
    
    console.log('Статус ответа:', response.status);
    
    if (!response.ok) {
      throw new Error(`Не удалось загрузить проекты. Статус: ${response.status}`);
    }
    
    cachedProjects = await response.json();
    console.log('Загружено проектов:', cachedProjects.length);
    return cachedProjects;
  } catch (error) {
    console.error('Ошибка загрузки проектов:', error);
    console.error('URL:', API_BASE_URL);
    throw error;
  }
};

export const getProjects = async (minViews = 100) => {
  const allProjects = await loadAllProjects();
  return allProjects.filter(p => (p.views || 0) > minViews);
};

export const getProjectById = async (id) => {
  const projects = await loadAllProjects();
  const project = projects.find(p => p.id === parseInt(id));
  
  if (!project) {
    throw new Error('Проект не найден');
  }
  
  return project;
};

export const searchProjects = async (searchTerm) => {
  const projects = await loadAllProjects();
  
  if (!searchTerm || !searchTerm.trim()) {
    return projects;
  }
  
  const term = searchTerm.toLowerCase().trim();
  
  return projects.filter(p => 
    p.title?.toLowerCase().includes(term) || 
    p.authority?.toLowerCase().includes(term) ||
    p.type?.toLowerCase().includes(term) ||
    p.procedure?.toLowerCase().includes(term)
  );
};