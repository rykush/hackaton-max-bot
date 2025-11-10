import { Button, Panel, Container } from '@maxhub/max-ui';

const Profile = () => (
    <Container style={{ padding: '20px' }}>
        <h1 style={{ marginBottom: '20px' }}>
            Профиль
        </h1>
        <Panel style={{ padding: '20px' }}>
            <Button
                appearance="themed"
                mode="primary"
                onClick={() => {}}
                size="medium"
            >
                Настройки профиля
            </Button>
        </Panel>
    </Container>
);

export default Profile;