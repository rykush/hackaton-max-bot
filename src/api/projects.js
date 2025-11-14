import projectsData from '../../public/projects.json';

let cachedProjects = null;

const loadAllProjects = async () => {
  if (cachedProjects) {
    return cachedProjects;
  }

  try {
    // Используем импортированные данные
    cachedProjects = projectsData;
    return projectsData;
  } catch (error) {
    console.error('Ошибка загрузки проектов:', error);
    throw error;
  }
};

export const getProjects = async (limit = 10) => {
  try {
    const allProjects = await loadAllProjects();
    return allProjects.slice(0, limit);
  } catch (error) {
    console.error('Ошибка в getProjects:', error);
    throw error;
  }
};

export const getProjectById = async (id) => {
  try {
    const allProjects = await loadAllProjects();
    return allProjects.find(project => project.id === id);
  } catch (error) {
    console.error('Ошибка в getProjectById:', error);
    throw error;
  }
};

export const searchProjects = async (query) => {
  try {
    const allProjects = await loadAllProjects();
    const lowerQuery = query.toLowerCase();
    
    return allProjects.filter(project => 
      project.title.toLowerCase().includes(lowerQuery) ||
      project.authority.toLowerCase().includes(lowerQuery) ||
      (project.type && project.type.toLowerCase().includes(lowerQuery))
    );
  } catch (error) {
    console.error('Ошибка в searchProjects:', error);
    throw error;
  }
};

export const getFilterOptions = async () => {
  try {
    const allProjects = await loadAllProjects();
    
    return {
      authorities: [...new Set(allProjects.map(p => p.authority))].sort(),
      types: [...new Set(allProjects.map(p => p.type))].sort(),
      statuses: [...new Set(allProjects.map(p => p.status))].sort(),
      procedures: [...new Set(allProjects.map(p => p.procedure))].sort()
    };
  } catch (error) {
    console.error('Ошибка в getFilterOptions:', error);
    throw error;
  }
};

export const clearCache = () => {
  cachedProjects = null;
};