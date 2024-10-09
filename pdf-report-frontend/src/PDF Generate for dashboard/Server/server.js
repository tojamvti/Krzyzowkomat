const express = require('express');
const PDFDocument = require('pdfkit');
const fs = require('fs');
const cors = require('cors');
const path = require('path');

const app = express();
app.use(cors());

app.get('/generate-pdf', (req, res) => {
    // Tworzymy nowy dokument PDF
    const doc = new PDFDocument();

    // Ustawienia nagłówków odpowiedzi
    res.setHeader('Content-type', 'application/pdf');
    res.setHeader('Content-disposition', 'attachment; filename="raport.pdf"');

    // Generowanie zawartości PDF
    doc.text('Statystyki Raportu', { align: 'center' });
    doc.text('----------------------------');
    doc.text('Dane statystyczne:');
    doc.text('Ilość użyć aplikacji: 120');
    doc.text('Ilość Wygenerowanych Zdjęć: 20000');
    doc.text('Średnia ilość nowych użytkowników dziennie: 24');

    // Wysłanie dokumentu do użytkownika
    doc.pipe(res);
    doc.end();
});

app.listen(5000, () => {
    console.log('Serwer działa na porcie 5000');
});
