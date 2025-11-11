
import { useState } from 'react';
import { Flex, ToolButton } from '@maxhub/max-ui';
import Home from './pages/Home';
import Search from './pages/Search';
import Dictionary from './pages/Dictionary';
import './App.css';

const App = () => {
    const [currentPage, setCurrentPage] = useState('home');

    const renderPage = () => {
        switch(currentPage) {
            case 'home': return <Home />;
            case 'search': return <Search />;
            case 'dictionary': return <Dictionary />;
            default: return <Home />;
        }
    };

    return (
        <div className="app-wrapper">
            <div className="app-container">
                {renderPage()}
            </div>

            <div className="bottom-panel">
                <Flex direction="row" gap={8} justify="space-around" align="center">
                    <ToolButton
                        appearance={currentPage === 'home' ? 'accent' : 'default'}
                        onClick={() => setCurrentPage('home')}
                    >
                        🏠 Главная
                    </ToolButton>
                    <ToolButton
                        appearance={currentPage === 'search' ? 'accent' : 'default'}
                        onClick={() => setCurrentPage('search')}
                    >
                        🔍 Поиск
                    </ToolButton>
                    <ToolButton
                        appearance={currentPage === 'dictionary' ? 'accent' : 'default'}
                        onClick={() => setCurrentPage('dictionary')}
                    >
                        📚 Словарь
                    </ToolButton>
                </Flex>
            </div>
        </div>
    );
};

export default App;