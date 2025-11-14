import { Button, Panel, Container, Grid } from '@maxhub/max-ui';
import { useState, useEffect } from 'react';
import { getProjects } from '../api/projects';

const Home = () => {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadProjects();
  }, []);

  const loadProjects = async () => {
    try {
      setLoading(true);
      const data = await getProjects(100);
      setProjects(data);
      setError(null);
    } catch (err) {
      setError('Не удалось загрузить проекты');
      console.error(err);
    } finally {
      setLoading(false);
    }
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
      
      <div style={{ marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <p style={{ margin: 0 }}>
          Проектов: {projects.length}
        </p>
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
        {projects.map((project) => (
          <Panel
            key={project.id}
            mode="primary"
            style={{
              padding: '20px',
              cursor: 'pointer',
              transition: 'transform 0.2s, box-shadow 0.2s',
              display: 'flex',
              flexDirection: 'column'
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
              color: '#666',
              marginBottom: '8px'
            }}>
              <div style={{ marginBottom: '4px' }}>
                <strong>Орган:</strong> {project.authority || 'Не указан'}
              </div>
              {project.type && (
                <div style={{ marginBottom: '4px' }}>
                  <strong>Тип:</strong> {project.type}
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
              color: '#999',
              paddingTop: '12px',
              borderTop: '1px solid #eee'
            }}>
              <span>👁 {project.views || 0} просмотров</span>
              <span>💬 {project.comments || 0} комментариев</span>
            </div>
          </Panel>
        ))}
      </Grid>

      {projects.length === 0 && (
        <Panel style={{ padding: '40px', textAlign: 'center' }}>
          <p>На данный момент проектов нет</p>
        </Panel>
      )}
    </Container>
  );
};

export default Home;