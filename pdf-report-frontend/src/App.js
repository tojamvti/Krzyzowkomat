import React from 'react';
import axios from 'axios';

function App() {
  const generatePDF = () => {
    axios({
      url: 'http://localhost:5000/generate-pdf',
      method: 'GET',
      responseType: 'blob', // Otrzymujemy plik jako blob
    })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement('a');
          link.href = url;
          link.setAttribute('download', 'raport.pdf');
          document.body.appendChild(link);
          link.click();
        })
        .catch((error) => {
          console.error('Błąd podczas generowania PDF:', error);
        });
  };

  return (
      <div className="App">
        <h1>Generowanie Raportu PDF</h1>
        <button onClick={generatePDF}>Pobierz Raport PDF</button>
      </div>
  );
}

export default App;
