import Database from 'better-sqlite3';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const db = new Database(path.join(__dirname, 'regulation_projects.db'));

try {
  const projects = db.prepare('SELECT * FROM projects ORDER BY views DESC').all();
  const publicDir = path.join(__dirname, 'public');
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir);
  }
  fs.writeFileSync(
    path.join(publicDir, 'projects.json'),
    JSON.stringify(projects, null, 2)
  );
  
  console.log(`Экспортировано ${projects.length} проектов в public/projects.json`);
} catch (error) {
  console.error('Ошибка экспорта:', error);
} finally {
  db.close();
}