import { Button, Panel, Container } from '@maxhub/max-ui';

const Home = () => (
    <Container style={{ padding: '20px' }}>
        <h1 style={{ marginBottom: '20px' }}>
            Главная страница
        </h1>
        <Panel style={{ padding: '20px' }}>
            <p>
                Добро пожаловать в приложение ОРВ!
            </p>
            <Button
                appearance="themed"
                mode="primary"
                onClick={() => {}}
                size="medium"
                style={{ marginTop: '20px' }}
            >
                Начать работу
            </Button>
        </Panel>
    </Container>
);

export default Home;