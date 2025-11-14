import express from 'express';
import cors from 'cors';
import Database from 'better-sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const db = new Database(path.join(__dirname, 'regulation_projects.db'));

app.use(cors());
app.use(express.json());

app.get('/api/projects', (req, res) => {
  try {
    const minViews = req.query.minViews || 100;
    const stmt = db.prepare(`
      SELECT * FROM projects 
      WHERE views > ? 
      ORDER BY views DESC
    `);
    const projects = stmt.all(minViews);
    res.json(projects);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/projects/:id', (req, res) => {
  try {
    const stmt = db.prepare('SELECT * FROM projects WHERE id = ?');
    const project = stmt.get(req.params.id);
    
    if (!project) {
      return res.status(404).json({ error: 'Проект не найден' });
    }
    
    res.json(project);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

app.get('/api/projects/search', (req, res) => {
  try {
    const searchTerm = req.query.q || '';
    const stmt = db.prepare(`
      SELECT * FROM projects 
      WHERE title LIKE ? OR authority LIKE ?
      ORDER BY views DESC
      LIMIT 50
    `);
    const projects = stmt.all(`%${searchTerm}%`, `%${searchTerm}%`);
    res.json(projects);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Сервер запущен на порту ${PORT}`);
});