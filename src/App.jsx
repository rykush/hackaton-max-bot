
import { useState } from 'react';
import { Flex, ToolButton } from '@maxhub/max-ui';
import Home from './pages/Home';
import Search from './pages/Search';
import Dictionary from './pages/Dictionary';
import discussionIcon from './assets/img/discussion.png';
import websiteIcon from './assets/img/website.png';
import dictionaryIcon from './assets/img/dictionary.png';
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
                        data-active={currentPage === 'home'}
                        className={currentPage === 'home' ? 'active' : ''}
                    >
                        <Flex direction="row" gap={6} align="center" justify="center">
                            <img src={discussionIcon} alt="Обсуждения" style={{ width: '15px', height: '15px', flexShrink: 0 }} />
                            <span>Обсуждения</span>
                        </Flex>
                    </ToolButton>
                    <ToolButton
                        appearance={currentPage === 'search' ? 'accent' : 'default'}
                        onClick={() => setCurrentPage('search')}
                        data-active={currentPage === 'search'}
                        className={currentPage === 'search' ? 'active' : ''}
                    >
                        <Flex direction="row" gap={6} align="center" justify="center">
                            <img src={websiteIcon} alt="Площадки" style={{ width: '15px', height: '15px', flexShrink: 0 }} />
                            <span>Площадки</span>
                        </Flex>
                    </ToolButton>
                    <ToolButton
                        appearance={currentPage === 'dictionary' ? 'accent' : 'default'}
                        onClick={() => setCurrentPage('dictionary')}
                        data-active={currentPage === 'dictionary'}
                        className={currentPage === 'dictionary' ? 'active' : ''}
                    >
                        <Flex direction="row" gap={6} align="center" justify="center">
                            <img src={dictionaryIcon} alt="Словарь" style={{ width: '15px', height: '15px', flexShrink: 0 }} />
                            <span>Словарь</span>
                        </Flex>
                    </ToolButton>
                </Flex>
            </div>
        </div>
    );
};

export default App;