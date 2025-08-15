// search.js für MoppDiary Suchseite
// Export- und Druckfunktionen für ausgewählte Cards

/**
 * Extrahiert ein Feld aus einer Card anhand des Label-Texts.
 * Wird aktuell nicht mehr für den Export verwendet, da die Daten als data-Attribute vorliegen.
 */
function extractCardField(card, labelText) {
  // Sucht das Feld anhand des Labels und gibt den Wert zurück
  const divs = card.querySelectorAll('div');
  for (const div of divs) {
    if (div.innerText.startsWith(labelText)) {
      // Label entfernen, Wert trimmen
      return div.innerText.replace(labelText, '').trim();
    }
  }
  return '';
}

/**
 * Exportiert die ausgewählten Cards als PDF.
 * Die Daten werden aus den data-Attributen der Card-Bodies ausgelesen.
 * Dateianhänge werden als Liste ausgegeben.
 */
function exportCardsToPDF(selectedCards) {
  async function runExport() {
    console.log('[PDF-Export] Starte Export, Anzahl ausgewählte Cards:', selectedCards.length);
    const { jsPDF } = window.jspdf || window;
    if (!jsPDF) {
      console.error('[PDF-Export] jsPDF nicht geladen!');
      return;
    }
    const doc = new jsPDF();
    let y = 15;
    doc.setFontSize(16);
    doc.text('MoppDiary - Ausgewählte Einträge', 10, y);
    y += 10;
    doc.setFontSize(11);
    if (!selectedCards.length) {
      doc.text('Keine Einträge ausgewählt.', 10, y);
      console.warn('[PDF-Export] Keine Einträge ausgewählt.');
    } else {
      for (const [idx, card] of selectedCards.entries()) {
        const title = card.getAttribute('data-title') || '';
        const kategorie = card.getAttribute('data-category') || '';
        const stimmung = card.getAttribute('data-mood') || '';
        const datum = card.getAttribute('data-date') || '';
        const beteiligte = card.getAttribute('data-people') || '';
        const inhalt = card.getAttribute('data-content') || '';
        const attachments = card.getAttribute('data-attachments') || '';
        const taskid = card.getAttribute('data-taskid') || '';
        console.log(`[PDF-Export] Card ${idx}:`, { title, kategorie, stimmung, datum, beteiligte, inhalt, attachments, taskid });
        let text = `Titel: ${title}\nKategorie: ${kategorie}\nStimmung: ${stimmung}\nDatum: ${datum}\nBeteiligte: ${beteiligte}\nInhalt: ${inhalt}`;
        text = text.replace(/([\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}\u{1FA70}-\u{1FAFF}\u{1F1E6}-\u{1F1FF}])/gu, '');
        const maxWidth = 180;
        const lines = doc.splitTextToSize(text, maxWidth);
        doc.text(lines, 10, y);
        y += lines.length * 7 + 8;
        // Bilder synchron laden und einfügen
        if (attachments.trim()) {
          const files = attachments.split(',').map(f => f.trim());
          let hasImage = false;
          for (const filename of files) {
            if (/\.(jpg|jpeg|png|gif)$/i.test(filename)) {
              hasImage = true;
              const imgUrl = `/attachments/${taskid}/${filename}`;
              console.log(`[PDF-Export] Versuche Bild zu laden:`, imgUrl);
              try {
                const dataUrl = await fetch(imgUrl)
                  .then(r => {
                    if (!r.ok) throw new Error(`HTTP ${r.status}`);
                    return r.blob();
                  })
                  .then(blob => new Promise(res => {
                    const reader = new FileReader();
                    reader.onload = () => res(reader.result);
                    reader.readAsDataURL(blob);
                  }));
                const img = new Image();
                img.src = dataUrl;
                await new Promise(resolve => { img.onload = resolve; });
                // PDF-Seite: ca. 180mm breit, 270mm hoch (A4, jsPDF Standard)
                const pdfMaxWidth = 180; // mm
                const pdfMaxHeight = 120; // mm
                // Umrechnung von Pixel zu mm (jsPDF: 1px = 0.264583 mm)
                let w = img.width * 0.264583;
                let h = img.height * 0.264583;
                // Begrenzung auf PDF-Seite
                if (w > pdfMaxWidth) {
                  h = h * (pdfMaxWidth / w);
                  w = pdfMaxWidth;
                }
                if (h > pdfMaxHeight) {
                  w = w * (pdfMaxHeight / h);
                  h = pdfMaxHeight;
                }
                doc.addImage(dataUrl, 'JPEG', 10, y, w, h);
                console.log(`[PDF-Export] Bild eingefügt: ${filename}, Größe: ${w}x${h}mm`);
                y += h + 8;
                if (y > 260) { doc.addPage(); y = 15; }
              } catch (e) {
                console.error(`[PDF-Export] Fehler beim Bild-Laden: ${filename}`, e);
                doc.text(`Bild konnte nicht geladen werden: ${filename}`, 10, y);
                y += 10;
              }
            }
          }
          // Falls keine Bilder, einfach Dateinamen als Text
          if (!hasImage) {
            doc.text(`Dateianhänge: ${attachments}`, 10, y);
            console.log(`[PDF-Export] Keine Bilder, Dateianhänge als Text:`, attachments);
            y += 10;
            if (y > 260) { doc.addPage(); y = 15; }
          }
        } else {
          if (y > 260) { doc.addPage(); y = 15; }
        }
      }
    }
    try {
      doc.save('MoppDiary_Auswahl.pdf');
      console.log('[PDF-Export] PDF erfolgreich gespeichert.');
    } catch (e) {
      console.error('[PDF-Export] Fehler beim PDF-Speichern:', e);
    }
  }
  // jsPDF dynamisch laden, falls noch nicht vorhanden
  if (typeof window.jsPDF === 'undefined' || typeof window.jspdf === 'undefined') {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
    script.onload = runExport;
    document.body.appendChild(script);
    return;
  }
  runExport();
}

/**
 * Exportiert die ausgewählten Cards als CSV.
 * Die Daten werden aus den data-Attributen der Card-Bodies ausgelesen.
 * Dateianhänge werden als Spalte ausgegeben.
 */
function exportCardsToCSV(selectedCards) {
  if (!selectedCards.length) { alert('Keine Einträge ausgewählt!'); return; }
  let csv = 'Titel;Kategorie;Stimmung;Datum;Beteiligte;Inhalt;Dateianhänge\n';
  function escapeCSV(val) {
    if (val == null) return '';
    val = String(val);
    // Doppelte Anführungszeichen im Feld verdoppeln
    val = val.replace(/"/g, '""');
    // Wenn Feld Semikolon, Zeilenumbruch oder Anführungszeichen enthält, in Anführungszeichen setzen
    if (/;|\n|\r|"/.test(val)) {
      return '"' + val + '"';
    }
    return val;
  }
  selectedCards.forEach(card => {
    const title = escapeCSV(card.getAttribute('data-title') || '');
    const kategorie = escapeCSV(card.getAttribute('data-category') || '');
    const stimmung = escapeCSV(card.getAttribute('data-mood') || '');
    const datum = escapeCSV(card.getAttribute('data-date') || '');
    const beteiligte = escapeCSV(card.getAttribute('data-people') || '');
    const inhalt = escapeCSV(card.getAttribute('data-content') || '');
    const attachments = escapeCSV(card.getAttribute('data-attachments') || '');
    csv += [title, kategorie, stimmung, datum, beteiligte, inhalt, attachments].join(';') + '\n';
  });
  // CSV mit BOM für Excel-Kompatibilität herunterladen
  const BOM = '\uFEFF';
  const blob = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = 'MoppDiary_Auswahl.csv';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

/**
 * Druckt die ausgewählten Cards.
 * Es wird nur die Card-Struktur (ohne Checkboxen und Auswählen-Label) angezeigt und gedruckt.
 * Nach dem Drucken wird das Original-HTML wiederhergestellt.
 */
function printSelectedCards(selectedCards) {
  if (!selectedCards.length) { alert('Keine Einträge ausgewählt!'); return; }
  // Cards für Druck generieren
  const printCards = selectedCards.map(cardBody => {
    const card = cardBody.closest('.card');
    const clone = card.cloneNode(true);
    // Checkboxen und "Auswählen"-Label entfernen
    const check = clone.querySelector('.form-check');
    if (check) check.remove();
    // Inline-Style von Bildern entfernen (damit Druck-CSS wirkt)
    clone.querySelectorAll('img').forEach(img => {
      img.removeAttribute('style');
    });
    return clone.outerHTML;
  }).join('');
  // Neues Fenster für Druck öffnen
  const printWin = window.open('', '_blank');
  printWin.document.write(`<!DOCTYPE html><html><head><title>Druckvorschau</title>
    <link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css'>
    <style>@media print { .card img { max-width: 100%; max-height: 900px; width: auto !important; height: auto !important; display: block; margin: 8px auto; } }
    .card img { max-width: 100%; max-height: 900px; width: auto !important; height: auto !important; display: block; margin: 8px auto; }
    .close-print-btn { position: fixed; top: 18px; right: 28px; z-index: 9999; font-size: 1.15rem; }
    </style>
    </head><body class='container mt-5' style="font-family: 'Caveat', cursive; background: #fff;">
    <button class='btn btn-outline-danger close-print-btn' onclick='window.close()'>Fenster schließen ✖</button>
    <div class='container'>${printCards}</div>
    <script>window.onload = function() { window.print(); }<\/script>
    </body></html>`);
  printWin.document.close();
}

// Card-Auswahl und Toolbar-Funktionen
// Initialisiert die Auswahl-Checkboxen und die Button-Handler

document.addEventListener('DOMContentLoaded', function() {
  // Checkbox "Alle auswählen"
  const selectAll = document.getElementById('selectAllCards');
  // Alle Card-Checkboxen
  const cardCheckboxes = document.querySelectorAll('.card-select-checkbox');
  // Handler für "Alle auswählen"
  selectAll?.addEventListener('change', function() {
    cardCheckboxes.forEach(cb => cb.checked = selectAll.checked);
  });
  // Handler für Einzel-Checkboxen
  cardCheckboxes.forEach(cb => {
    cb.addEventListener('change', function() {
      if (!cb.checked) selectAll.checked = false;
      else if ([...cardCheckboxes].every(c => c.checked)) selectAll.checked = true;
    });
  });

  // Card-Klick setzt Checkbox (nur für Cards im Suchergebnis, nicht Toolbar)
  const resultCards = document.querySelectorAll('#searchCardsContainer .card');
  resultCards.forEach(card => {
    card.addEventListener('click', function(e) {
      // Wenn direkt auf die Checkbox oder das Label geklickt wurde, nichts tun
      if (e.target.classList.contains('card-select-checkbox') || e.target.classList.contains('form-check-label')) return;
      const checkbox = card.querySelector('.card-select-checkbox');
      if (checkbox) {
        checkbox.checked = !checkbox.checked;
        checkbox.dispatchEvent(new Event('change'));
      }
    });
  });

  /**
   * Gibt die Card-Bodies der ausgewählten Cards zurück.
   */
  function getSelectedCards() {
    return [...cardCheckboxes].filter(cb => cb.checked).map(cb => cb.closest('.card').querySelector('.card-body'));
  }

  // PDF Export Button
  document.getElementById('exportPdfBtn')?.addEventListener('click', function() {
    const selected = getSelectedCards();
    if (!selected.length) { alert('Keine Einträge ausgewählt!'); return; }
    exportCardsToPDF(selected);
  });

  // CSV Export Button
  document.getElementById('exportCsvBtn')?.addEventListener('click', function() {
    const selected = getSelectedCards();
    if (!selected.length) { alert('Keine Einträge ausgewählt!'); return; }
    exportCardsToCSV(selected);
  });

  // Drucken Button
  document.getElementById('printBtn')?.addEventListener('click', function() {
    const selected = getSelectedCards();
    if (!selected.length) { alert('Keine Einträge ausgewählt!'); return; }
    printSelectedCards(selected);
  });
});
