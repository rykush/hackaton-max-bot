
import { Button, Panel, Container, Grid } from '@maxhub/max-ui';
import { useState, useEffect } from 'react';
import { getProjects } from '../api/projects';

const Home = () => {
  const [projects, setProjects] = useState([]);
  const [filteredProjects, setFilteredProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  const [selectedOkved, setSelectedOkved] = useState('all');
  const [selectedAuthority, setSelectedAuthority] = useState('all');
  

  const [okveds, setOkveds] = useState([]);
  const [authorities, setAuthorities] = useState([]);

  useEffect(() => {
    loadProjects();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [projects, selectedOkved, selectedAuthority]);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const data = await getProjects(100);
      const popularProjects = data.filter(p => p.views > 100);
      setProjects(popularProjects);

      const allOkveds = new Set();
      popularProjects.forEach(p => {
        if (Array.isArray(p.okveds)) {
          p.okveds.forEach(okved => allOkveds.add(okved));
        } else if (typeof p.okveds === 'string' && p.okveds) {
          allOkveds.add(p.okveds);
        }
      });
      
      const uniqueAuthorities = [...new Set(popularProjects.map(p => p.authority).filter(Boolean))];
      
      setOkveds(Array.from(allOkveds).sort());
      setAuthorities(uniqueAuthorities.sort());
      
      setError(null);
    } catch (err) {
      setError('Не удалось загрузить проекты');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...projects];
    
    if (selectedOkved !== 'all') {
      filtered = filtered.filter(p => {
        if (Array.isArray(p.okveds)) {
          return p.okveds.includes(selectedOkved);
        }
        return p.okveds === selectedOkved;
      });
    }
    
    if (selectedAuthority !== 'all') {
      filtered = filtered.filter(p => p.authority === selectedAuthority);
    }
    
    setFilteredProjects(filtered);
  };

  const resetFilters = () => {
    setSelectedOkved('all');
    setSelectedAuthority('all');
  };

  const handleProjectClick = (projectId) => {
    window.open(`https://regulation.gov.ru/projects/${projectId}`, '_blank');
  };

  const getStatusColor = (status) => {
    const statusColors = {
      'Публичные консультации': '#4CAF50',
      'Завершено': '#9E9E9E',
      'На рассмотрении': '#FF9800',
      'Принято': '#2196F3'
    };
    return statusColors[status] || '#757575';
  };

  if (loading) {
    return (
      <Container style={{ padding: '20px' }}>
        <h1 style={{ marginBottom: '20px' }}>Главная страница</h1>
        <Panel style={{ padding: '20px', textAlign: 'center' }}>
          <p>Загрузка проектов...</p>
        </Panel>
      </Container>
    );
  }

  if (error) {
    return (
      <Container style={{ padding: '20px' }}>
        <h1 style={{ marginBottom: '20px' }}>Главная страница</h1>
        <Panel style={{ padding: '20px', textAlign: 'center' }}>
          <p style={{ color: 'red' }}>{error}</p>
          <Button
            appearance="themed"
            mode="primary"
            onClick={loadProjects}
            size="medium"
            style={{ marginTop: '20px' }}
          >
            Попробовать снова
          </Button>
        </Panel>
      </Container>
    );
  }

  return (
    <Container style={{ padding: '20px' }}>
      <h1 style={{ marginBottom: '20px' }}>Популярные проекты нормативных актов</h1>
      


      <Panel mode="secondary" style={{ padding: '20px', borderRadius: '10px' , marginBottom: '20px'}}>
        <h3 style={{ margin: '0 0 15px 0', fontSize: '16px' }}>Фильтры</h3>
        
        <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap', marginBottom: '15px' }}>

          <div style={{ flex: '1', minWidth: '250px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '8px', 
              fontSize: '14px',
              fontWeight: '500'
            }}>
              Вид экономической деятельности (ОКВЭД):
            </label>
            <select
              value={selectedOkved}
              onChange={(e) => setSelectedOkved(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                fontSize: '14px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                backgroundColor: '#fff',
                cursor: 'pointer',
                transition: 'border-color 0.2s, box-shadow 0.2s',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = '#4CAF50';
                e.target.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.1)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = '#ddd';
                e.target.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
              }}
            >
              <option value="all">Все виды деятельности</option>
              {okveds.map(okved => (
                <option key={okved} value={okved}>{okved}</option>
              ))}
            </select>
          </div>

          <div style={{ flex: '1', minWidth: '250px' }}>
            <label style={{ 
              display: 'block', 
              marginBottom: '8px', 
              fontSize: '14px',
              fontWeight: '500'
            }}>
              Орган власти:
            </label>
            <select
              value={selectedAuthority}
              onChange={(e) => setSelectedAuthority(e.target.value)}
              style={{
                width: '100%',
                padding: '10px 12px',
                fontSize: '14px',
                borderRadius: '8px',
                border: '1px solid #ddd',
                backgroundColor: '#fff',
                cursor: 'pointer',
                transition: 'border-color 0.2s, box-shadow 0.2s',
                boxShadow: '0 1px 3px rgba(0,0,0,0.05)'
              }}
              onFocus={(e) => {
                e.target.style.borderColor = '#4CAF50';
                e.target.style.boxShadow = '0 0 0 3px rgba(76, 175, 80, 0.1)';
              }}
              onBlur={(e) => {
                e.target.style.borderColor = '#ddd';
                e.target.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
              }}
            >
              <option value="all">Все органы</option>
              {authorities.map(authority => (
                <option key={authority} value={authority}>{authority}</option>
              ))}
            </select>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
          <Button
            appearance="themed"
            mode="secondary"
            onClick={resetFilters}
            size="small"
            disabled={selectedOkved === 'all' && selectedAuthority === 'all'}
          >
            Сбросить фильтры
          </Button>
          
          <span style={{ fontSize: '14px', color: '#666' }}>
            Найдено: {filteredProjects.length} из {projects.length}
          </span>
        </div>
      </Panel>

      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'flex-end' }}>
        <Button
          appearance="themed"
          mode="secondary"
          onClick={loadProjects}
          size="small"
        >
          Обновить
        </Button>
      </div>

      <Grid
        align="start"
        cols={1}
        display="inline-grid"
        gapX={30}
        gapY={20}
        justify="start"
      >
        {filteredProjects.map((project) => (
          <Panel
            key={project.id}
            mode="primary"
            style={{
              padding: '20px',
              cursor: 'pointer',
              transition: 'transform 0.2s, box-shadow 0.2s',
              display: 'flex',
              flexDirection: 'column',
              borderRadius: '10px'
            }}
            onClick={() => handleProjectClick(project.id)}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-5px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(0,0,0,0.15)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            <div style={{ 
              display: 'inline-block',
              padding: '4px 12px',
              borderRadius: '12px',
              backgroundColor: getStatusColor(project.status),
              color: 'white',
              fontSize: '12px',
              fontWeight: '500',
              marginBottom: '12px',
              alignSelf: 'flex-start'
            }}>
              {project.status || 'Без статуса'}
            </div>

            <h3 style={{ 
              margin: '0 0 12px 0',
              fontSize: '16px',
              lineHeight: '1.4',
              overflow: 'hidden',
              display: '-webkit-box',
              WebkitLineClamp: 3,
              WebkitBoxOrient: 'vertical'
            }}>
              {project.title}
            </h3>

            <div style={{ 
              fontSize: '13px',
              color: '#cacacaff',
              marginBottom: '8px'
            }}>
              <div style={{ marginBottom: '4px' }}>
                <strong>Орган:</strong> {project.authority || 'Не указан'}
              </div>
            {project.okveds && (
              <div style={{ marginBottom: '4px' }}>
                <strong>ОКВЭД:</strong> {Array.isArray(project.okveds) ? project.okveds.join(', ') : project.okveds}
              </div>
            )}
              {project.procedure && (
                <div style={{ marginBottom: '4px' }}>
                  <strong>Процедура:</strong> {project.procedure}
                </div>
              )}
            </div>

            <div style={{ 
              display: 'flex',
              justifyContent: 'space-between',
              fontSize: '12px',
              color: '#cacacaff',
              paddingTop: '12px',
              borderTop: '1px solid #eee'
            }}>
              <span>👁 {project.views || 0} просмотров</span>
              <span>💬 {project.comments || 0} комментариев</span>
            </div>
          </Panel>
        ))}
      </Grid>

      {filteredProjects.length === 0 && (
        <Panel style={{ padding: '40px', textAlign: 'center' }}>
          <p>Проектов с выбранными фильтрами не найдено</p>
          <Button
            appearance="themed"
            mode="secondary"
            onClick={resetFilters}
            size="medium"
            style={{ marginTop: '15px' }}
          >
            Сбросить фильтры
          </Button>
        </Panel>
      )}
    </Container>
  );
};

export default Home;