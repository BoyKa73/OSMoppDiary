// main.js - Alle Skripte aus index.html zusammengeführt
// --- Validierung der Dateiendungen beim Datei-Upload (Neuer Eintrag) ---
document.addEventListener('DOMContentLoaded', function() {
  const allowedExtensions = ["png","jpg","jpeg","gif","pdf","txt","odf","ods","doc","docx"];
  const fileInput = document.querySelector('input[type="file"][name="attachments"]');
  if (fileInput) {
    fileInput.addEventListener('change', function(e) {
      const files = Array.from(fileInput.files);
      const invalid = files.filter(f => {
        const ext = f.name.split('.').pop().toLowerCase();
        return !allowedExtensions.includes(ext);
      });
      if (invalid.length > 0) {
        alert('Folgende Dateien sind nicht erlaubt:\n' + invalid.map(f => f.name).join('\n') + '\nErlaubte Formate: ' + allowedExtensions.join(', '));
        fileInput.value = '';
      }
    });
  }
});
//
// Dieses Skript steuert die wichtigsten Interaktionen der MoppDiary-Webapp.
// Es enthält Funktionen für Kalender, Orga-Box-Filter, Export, Druck und viele UI-Features.
// Die Kommentare helfen Anfängern, die Logik und die wichtigsten Abläufe zu verstehen.
// Setze Standardwerte für Start- und Endzeit im Eintragsformular
// Setzt die Standardwerte für Start- und Endzeit im Eintragsformular auf die aktuelle Zeit und +1 Stunde
document.addEventListener('DOMContentLoaded', function() {
  var startInput = document.getElementById('startTimeInput');
  var endInput = document.getElementById('endTimeInput');
  if (startInput && endInput) {
    var now = new Date();
    var pad = n => n.toString().padStart(2, '0');
    var startStr = pad(now.getHours()) + ':' + pad(now.getMinutes());
    var endDate = new Date(now.getTime() + 60 * 60 * 1000);
    var endStr = pad(endDate.getHours()) + ':' + pad(endDate.getMinutes());
    startInput.value = startStr;
    endInput.value = endStr;
  }
});


// Downcounter Navbar: Passt das Hintergrund-Design je nach Dark Mode an
document.addEventListener('DOMContentLoaded', function() {
  function setDowncounterDarkMode() {
    var downNav = document.getElementById('downcounter-navbar-bg');
    if (downNav) {
      if (document.body.classList.contains('dark-mode')) {
        downNav.style.background = 'linear-gradient(90deg, rgba(30,30,40,0.92) 0%, rgba(160,160,200,0.18) 100%)';
        downNav.style.backdropFilter = 'blur(3.5px)';
      } else {
        downNav.style.background = 'linear-gradient(90deg, rgba(75,54,124,0.12) 0%, rgba(230,230,250,0.80) 100%)';
        downNav.style.backdropFilter = 'blur(2px)';
      }
    }
  }
  setDowncounterDarkMode();
  // Beobachtet Änderungen am Body (Dark Mode Toggle)
  const observer = new MutationObserver(setDowncounterDarkMode);
  observer.observe(document.body, { attributes: true, attributeFilter: ['class'] });
});

// Countdown für Events: Zeigt die verbleibende Zeit bis zu einem Datum an
function setupCountdowns() {
  document.querySelectorAll('.countdown').forEach(function (el) {
    // RESTTAGE BIS WINTERFERIEN: Backend-Wert nicht überschreiben!
    if (el.dataset.eventId === "44" || (el.textContent && el.textContent.includes("WINTERFERIEN"))) {
      // Nur die Stunden/Minuten/Sekunden aktualisieren, Tage bleibt wie gerendert
      const container = el.closest('.col-md-3');
      const hoursElement = container.querySelector('.hours');
      const minutesElement = container.querySelector('.minutes');
      const secondsElement = container.querySelector('.seconds');
      function updateTime() {
        const target = new Date(el.dataset.date);
        const now = new Date();
        let diff = target - now;
        if (diff < 0) {
          hoursElement.textContent = "00";
          minutesElement.textContent = "00";
          secondsElement.textContent = "00";
          return;
        }
        diff = diff % 86400000;
        const hours = Math.floor(diff / 3600000).toString().padStart(2, '0');
        diff = diff % 3600000;
        const minutes = Math.floor(diff / 60000).toString().padStart(2, '0');
        const seconds = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
        hoursElement.textContent = hours;
        minutesElement.textContent = minutes;
        secondsElement.textContent = seconds;
        setTimeout(updateTime, 1000);
      }
      updateTime();
      return;
    }
    // Standard: Countdown wie bisher
    const target = new Date(el.dataset.date);
    const container = el.closest('.col-md-3');
    const daysElement = container.querySelector('.days-count');
    const hoursElement = container.querySelector('.hours');
    const minutesElement = container.querySelector('.minutes');
    const secondsElement = container.querySelector('.seconds');

    function update() {
      const now = new Date();
      let diff = target - now;
      if (diff < 0) {
        daysElement.textContent = "0";
        hoursElement.textContent = "00";
        minutesElement.textContent = "00";
        secondsElement.textContent = "00";
        return;
      }
      const days = Math.floor(diff / 86400000);
      diff = diff % 86400000;
      const hours = Math.floor(diff / 3600000).toString().padStart(2, '0');
      diff = diff % 3600000;
      const minutes = Math.floor(diff / 60000).toString().padStart(2, '0');
      const seconds = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
      daysElement.textContent = days;
      hoursElement.textContent = hours;
      minutesElement.textContent = minutes;
      secondsElement.textContent = seconds;
      setTimeout(update, 1000);
    }
    update();
  });
}
document.addEventListener("DOMContentLoaded", setupCountdowns);

// Aktiviert/Deaktiviert das Datumseingabefeld je nach gewählter Löschoption
function setupDeleteActionRadio() {
  document.querySelectorAll('input[name="delete_action"]').forEach(radio => {
    radio.addEventListener('change', function() {
      const dateInput = document.querySelector('input[name="delete_date"]');
      dateInput.disabled = this.id !== 'deleteOldEntries';
    });
  });
}
document.addEventListener("DOMContentLoaded", setupDeleteActionRadio);

// Zeigt eine Sicherheitsabfrage beim Löschen von Einträgen/Dateien/Anhängen
function confirmDelete() {
  const selectedAction = document.querySelector('input[name="delete_action"]:checked').value;
  let message = '';
  switch(selectedAction) {
    case 'all':
      message = 'Bist du sicher, dass du ALLE Einträge löschen möchtest?';
      break;
    case 'old_entries':
      const date = document.querySelector('input[name="delete_date"]').value;
      message = `Bist du sicher, dass du ALLE Einträge vor dem ${date} löschen möchtest?`;
      break;
    case 'old_attachments':
      message = 'Bist du sicher, dass du alle alten Anhänge löschen möchtest?';
      break;
    case 'all_attachments':
      message = 'Bist du sicher, dass du ALLE Anhänge löschen möchtest?';
      break;
    case 'old_files':
      message = 'Bist du sicher, dass du alle alten Dateien löschen möchtest?';
      break;
    case 'all_files':
      message = 'Bist du sicher, dass du ALLE Dateien löschen möchtest?';
      break;
  }
  return confirm(message + ' Diese Aktion kann nicht rückgängig gemacht werden!');
}

// Initialisiert den FullCalendar und bindet die Kalenderfunktionen ein
function setupCalendar() {
  const calendarEl = document.getElementById('calendar');
  const calendarCard = document.getElementById('calendarCard');
  window.moppCalendar = null;
  let calendarInitialized = false;
  if (calendarCard) {
    calendarCard.addEventListener('shown.bs.collapse', function () {
      if (!calendarInitialized) {
        window.moppCalendar = new FullCalendar.Calendar(calendarEl, {
          initialView: 'timeGridWeek',
          firstDay: 1,
          locale: 'de',
          headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'timeGridDay,timeGridWeek,dayGridMonth'
          },
          events: '/events',
          height: 'auto',
          editable: true,
          eventStartEditable: true,
          eventDurationEditable: true,
          eventResizableFromStart: true,
          dragScroll: true,
          dateClick: function(info) {
            // Felder im Eintragsformular vorbefüllen
            const startDateInput = document.querySelector('input[name="start_date"]');
            const endDateInput = document.querySelector('input[name="end_date"]');
            const startTimeInput = document.getElementById('startTimeInput');
            const endTimeInput = document.getElementById('endTimeInput');
            // All-Day-Häkchen setzen, wenn allDay true
            const allDayCheckbox = document.getElementById('allDayCheckbox');
            if (allDayCheckbox) {
              if (info.allDay && !allDayCheckbox.checked) {
                allDayCheckbox.click();
              } else if (!info.allDay && allDayCheckbox.checked) {
                allDayCheckbox.click();
              }
            }
            if (startDateInput) startDateInput.value = info.dateStr.split('T')[0];
            if (endDateInput) endDateInput.value = info.dateStr.split('T')[0];
            if (info.dateStr.includes('T') && startTimeInput) {
              startTimeInput.value = info.dateStr.split('T')[1].slice(0,5);
            }
            if (endTimeInput) endTimeInput.value = '';
            // Formular "Neuer Eintrag" aufklappen und Fokus+Scroll auf Titelfeld setzen
            const entryCollapse = document.getElementById('entryCardContent');
            if (entryCollapse && !entryCollapse.classList.contains('show')) {
              const bsCollapse = bootstrap.Collapse.getOrCreateInstance(entryCollapse);
              bsCollapse.show();
              // Fokus und Scroll nach Animation setzen
              setTimeout(() => {
                const titleInput = document.querySelector('input[name="title"]');
                if (titleInput) {
                  titleInput.focus();
                  titleInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
              }, 350);
            } else {
              const titleInput = document.querySelector('input[name="title"]');
              if (titleInput) {
                titleInput.focus();
                titleInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
              }
            }
          },
          selectable: true,
          select: function(info) {
            // Felder im Eintragsformular vorbefüllen
            const startDateInput = document.querySelector('input[name="start_date"]');
            const endDateInput = document.querySelector('input[name="end_date"]');
            const startTimeInput = document.getElementById('startTimeInput');
            const endTimeInput = document.getElementById('endTimeInput');
            // All-Day-Häkchen setzen, wenn allDay true
            const allDayCheckbox = document.getElementById('allDayCheckbox');
            if (allDayCheckbox) {
              if (info.allDay && !allDayCheckbox.checked) {
                allDayCheckbox.click();
              } else if (!info.allDay && allDayCheckbox.checked) {
                allDayCheckbox.click();
              }
            }
            if (startDateInput) startDateInput.value = info.startStr.split('T')[0];
            if (endDateInput) endDateInput.value = info.endStr.split('T')[0];
            if (info.startStr.includes('T') && startTimeInput) {
              startTimeInput.value = info.startStr.split('T')[1].slice(0,5);
            }
            if (info.endStr.includes('T') && endTimeInput) {
              endTimeInput.value = info.endStr.split('T')[1].slice(0,5);
            }
            // Formular "Neuer Eintrag" aufklappen und Fokus+Scroll auf Titelfeld setzen
            const entryCollapse = document.getElementById('entryCardContent');
            if (entryCollapse && !entryCollapse.classList.contains('show')) {
              const bsCollapse = bootstrap.Collapse.getOrCreateInstance(entryCollapse);
              bsCollapse.show();
              setTimeout(() => {
                const titleInput = document.querySelector('input[name="title"]');
                if (titleInput) {
                  titleInput.focus();
                  titleInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
              }, 350);
            } else {
              const titleInput = document.querySelector('input[name="title"]');
              if (titleInput) {
                titleInput.focus();
                titleInput.scrollIntoView({ behavior: 'smooth', block: 'center' });
              }
            }
          },
          eventDrop: function(info) {
            // Drag&Drop: Änderungen per AJAX an das Backend senden
            fetch(`/edit_event/${info.event.id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                start_date: info.event.start.toISOString(),
                end_date: info.event.end ? info.event.end.toISOString() : info.event.start.toISOString()
              })
            })
            .then(response => {
              if (!response.ok) {
                alert('Fehler beim Verschieben des Termins!');
                info.revert();
              }
            })
            .catch(() => {
              alert('Netzwerkfehler!');
              info.revert();
            });
          },
          eventResize: function(info) {
            // Resize: Änderungen per AJAX an das Backend senden
            fetch(`/resize/${info.event.id}`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
              },
              body: JSON.stringify({
                start_date: info.event.start.toISOString(),
                end_date: info.event.end ? info.event.end.toISOString() : info.event.start.toISOString()
              })
            })
            .then(response => {
              if (!response.ok) {
                alert('Fehler beim Ändern der Dauer!');
                info.revert();
              }
            })
            .catch(() => {
              alert('Netzwerkfehler!');
              info.revert();
            });
          },
          eventClick: function (info) {
            // Öffnet ein Modal mit Details zum Eintrag, inkl. Anhänge und Bearbeiten/Löschen
            const id = info.event.id;
            const props = info.event.extendedProps || {};
            const isTask = !!props.content || !!props.category;
            // Daten extrahieren
            const title = info.event.title || '';
            const content = props.content || '';
            const category = props.category || '';
            const mood = props.mood || '';
            const people = props.people || '';
            const color = info.event.color || '';
            const created = props.created || '';
            const startDate = info.event.start ? info.event.start.toLocaleDateString() : '';
            const startTime = info.event.start ? info.event.start.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
            const endDate = info.event.end ? info.event.end.toLocaleDateString() : '';
            const endTime = info.event.end ? info.event.end.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '';
            const attachments = props.attachments || [];
            let attachmentsHtml = "";
            if (attachments.length) {
              attachmentsHtml += `<div class="mt-3"><strong>📎 Anhänge:</strong><div class="row g-3">`;
              attachments.forEach(file => {
                const ext = file.split('.').pop().toLowerCase();
                if (["jpg", "jpeg", "png", "gif"].includes(ext)) {
                  attachmentsHtml += `
                    <div class="col-md-4">
                      <img src="/static/uploads/${file}" class="img-fluid rounded border" alt="Bild">
                    </div>`;
                } else {
                  attachmentsHtml += `
                    <div class="col-md-4">
                      <a href="/static/uploads/${file}" target="_blank" class="btn btn-outline-dark w-100">📄 ${file}</a>
                    </div>`;
                }
              });
              attachmentsHtml += `</div></div>`;
            }
            let modalBody = `<p><strong>Titel:</strong> ${title}</p>`;
            if (isTask) {
              modalBody += `<p><strong>Inhalt:</strong> ${content}</p>`;
              modalBody += `<p><strong>Kategorie:</strong> ${category}</p>`;
              modalBody += `<p><strong>Stimmung:</strong> ${mood}</p>`;
              modalBody += `<p><strong>Beteiligte:</strong> ${people}</p>`;
            }
            modalBody += `<p><strong>Start:</strong> ${startDate} ${startTime}</p>`;
            modalBody += `<p><strong>Ende:</strong> ${endDate} ${endTime}</p>`;
            modalBody += `<p><strong>Erstellt am:</strong> ${created}</p>`;
            modalBody += attachmentsHtml;
            modalBody += `<div class="form-check mt-3">
                        <input class="form-check-input" type="checkbox" name="selected" value="${id}" checked>
                        <label class="form-check-label">Für PDF auswählen</label>
                      </div>`;
            const modalHtml = `
              <div class="modal fade" id="taskModal" tabindex="-1">
                <div class="modal-dialog">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">${isTask ? '📌 Eintrag' : '📅 Ereignis'} am ${startDate} ${startTime}</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                      ${modalBody}
                    </div>
                    <div class="modal-footer d-flex justify-content-between">
                      <div>
                        <a href="/edit/${id}" class="btn btn-primary me-2">✏️ Bearbeiten</a>
                        <button type="button" class="btn btn-danger" onclick="deleteEntry('${id}');">🗑️ Löschen</button>
                      </div>
                      <div>
                        <button type="button" class="btn btn-outline-dark" id="exportPdfBtn">📄 Exportieren</button>
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Schließen</button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            `;
            document.getElementById("taskModal")?.remove();
            document.body.insertAdjacentHTML("beforeend", modalHtml);
            const modal = new bootstrap.Modal(document.getElementById("taskModal"));
            modal.show();
            // PDF-Export-Button Handler
            setTimeout(() => {
              const exportBtn = document.getElementById("exportPdfBtn");
              if (exportBtn) {
                exportBtn.onclick = function() {
                  // jsPDF dynamisch laden, falls nicht vorhanden
                  if (typeof window.jsPDF === 'undefined') {
                    const script = document.createElement('script');
                    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
                    script.onload = () => exportModalToPDF();
                    document.body.appendChild(script);
                  } else {
                    exportModalToPDF();
                  }
                };
              }
            }, 300);
            // PDF-Export-Funktion für Modal
            function exportModalToPDF() {
              const { jsPDF } = window.jspdf || window;
              const doc = new jsPDF();
              let y = 15;
              doc.setFontSize(16);
              doc.text('MoppDiary - Eintrag', 10, y);
              y += 10;
              doc.setFontSize(11);
              // Modal-Daten extrahieren
              const modal = document.getElementById('taskModal');
              if (!modal) return;
              const body = modal.querySelector('.modal-body');
              if (!body) return;
              // Nur <p>-Elemente auslesen, Checkbox wird ignoriert
              body.querySelectorAll('p').forEach(el => {
                let text = el.innerText.replace(/\s+/g, ' ').trim();
                text = text.replace(/\u{1F600}-\u{1F64F}/gu, ''); // Emojis grob entfernen
                if (text) {
                  doc.text(text, 10, y);
                  y += 8;
                  if (y > 280) {
                    doc.addPage();
                    y = 15;
                  }
                }
              });
              doc.save('MoppDiary_Eintrag.pdf');
            }
          }
        });
        window.moppCalendar.render();
        calendarInitialized = true;
      } else {
        window.moppCalendar.render();
      }
    });
    window.addEventListener('resize', function () {
      if (calendarInitialized) {
        calendar.render();
      }
    });
  }
}
document.addEventListener("DOMContentLoaded", setupCalendar);

// Löscht einen Eintrag nach Bestätigung und entfernt ihn aus dem Kalender
function deleteEntry(id) {
  if(confirm('Diesen Eintrag wirklich löschen?')) {
    fetch(`/delete/${id}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      }
    })
    .then(response => {
      if(response.ok) {
        // Modal schließen
        const modalEl = document.getElementById('taskModal');
        if (modalEl) {
          const modal = bootstrap.Modal.getInstance(modalEl);
          modal.hide();
          setTimeout(() => modalEl.remove(), 500);
        }
        // Event aus FullCalendar entfernen
        if (window.moppCalendar) {
          const event = window.moppCalendar.getEventById(id);
          if (event) event.remove();
        }
      } else {
        alert('Löschen fehlgeschlagen');
      }
    })
    .catch(error => console.error('Error:', error));
  }
}

// Cookie-Helper
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

// Synchronisiere beide Toggle-Buttons und Theme
function syncThemeToggles(theme) {
    const isDarkMode = theme === 'dark';
    
    const navbarToggle = document.getElementById('styleToggle');
    navbarToggle.innerHTML = isDarkMode ? '☀️' : '🌙';
    navbarToggle.setAttribute('title', isDarkMode ? 'Light Mode aktivieren' : 'Dark Mode aktivieren');
    
    const darkModeSwitch = document.getElementById('darkModeSwitch');
    if (darkModeSwitch) darkModeSwitch.checked = isDarkMode;
    
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        document.documentElement.setAttribute('data-bs-theme', 'dark');
        localStorage.setItem('darkMode', 'enabled');
    } else {
        document.body.classList.remove('dark-mode');
        document.documentElement.setAttribute('data-bs-theme', 'light');
        localStorage.setItem('darkMode', 'disabled');
    }
}

// Toggle-Funktion für Navbar-Button
function toggleStyle() {
    const currentTheme = document.documentElement.getAttribute('data-bs-theme') || 
                        (document.body.classList.contains('dark-mode') ? 'dark' : 'light');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    syncThemeToggles(newTheme);
    
    fetch('/update_style', {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        body: `dark_mode=${newTheme === 'dark' ? 'on' : 'off'}&redirect_to=${window.location.pathname}`
    });
}

// Initialisierung
document.addEventListener("DOMContentLoaded", function () {
    const savedTheme = getCookie('theme') || 
                      (localStorage.getItem('darkMode') === 'enabled' ? 'dark' : 'light') || 
                      'light';
    syncThemeToggles(savedTheme);
    
    // Ihre bestehenden Initialisierungen bleiben unverändert
    loadEvents();
    initOrgaBoxFilter(); 
    initCalendar();
});

  // --- Orga-Box Kalender-Filter: Events laden und Filterfunktion ---
  window.moppEntries = [];
  fetch('/events')
    .then(res => res.json())
    .then(data => {
      window.moppEntries = data;
      setupOrgaBoxFilter();
      setupCalendarWithEntries(data);
 });


// Initialisiert den Kalender mit geladenen Events (z. B. nach Filterung)
function setupCalendarWithEntries(entries) {
  // Initialisiere FullCalendar mit den geladenen Events
  const calendarEl = document.getElementById('calendar');
  if (!calendarEl) return;
  if (window.moppCalendar) {
    window.moppCalendar.removeAllEvents();
    window.moppCalendar.addEventSource(entries);
    return;
  }
  window.moppCalendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'timeGridWeek',
    firstDay: 1,
    locale: 'de',
    headerToolbar: {
      left: 'prev,next today',
      center: 'title',
      right: 'timeGridDay,timeGridWeek,dayGridMonth'
    },
    events: entries,
    height: 'auto',
    editable: true,
    eventStartEditable: true,
    eventDurationEditable: true,
    eventResizableFromStart: true,
    dragScroll: true
    // ...weitere Optionen wie im Original
  });
  window.moppCalendar.render();
}

// Orga-Box: Filtert Einträge nach Suchbegriff und Stimmung, zeigt Trefferliste und Export/Druck-Buttons
function setupOrgaBoxFilter() {
  // Button: Gefilterte löschen
  document.getElementById('orgaDeleteFilteredBtn')?.addEventListener('click', function() {
    const entries = Array.from(resultsList.querySelectorAll('li')).filter(li => !li.classList.contains('text-muted'));
    if (!entries.length) {
      alert('Keine Treffer zum Löschen!');
      return;
    }
    if (!confirm('Möchtest du wirklich ALLE gefilterten Einträge löschen? Diese Aktion kann nicht rückgängig gemacht werden!')) return;
    entries.forEach(li => {
      const id = li.dataset.id;
      if (id) deleteEntry(id);
    });
  });
  const searchInput = document.getElementById('orgaSearchInput');
  const moodSelect = document.getElementById('orgaMoodSelect');
  const categorySelect = document.getElementById('orgaCategorySelect');
  const startDateInput = document.getElementById('orgaStartDate');
  const endDateInput = document.getElementById('orgaEndDate');
  const resultsList = document.getElementById('orgaResultsList');
  if (!searchInput || !moodSelect || !categorySelect || !resultsList) return;

  // Filtert die Einträge nach Suchtext und Stimmung
  function filterEntries() {
    const search = searchInput.value.trim().toLowerCase();
    let mood = moodSelect.value;
    let category = categorySelect.value;
    let startDate = startDateInput && startDateInput.value ? new Date(startDateInput.value) : null;
    let endDate = endDateInput && endDateInput.value ? new Date(endDateInput.value) : null;
    const filtered = window.moppEntries.filter(e => {
      let match = true;
      if (search) {
        match = (
          (e.title && e.title.toLowerCase().includes(search)) ||
          (e.content && e.content.toLowerCase().includes(search)) ||
          (e.people && e.people.toLowerCase().includes(search))
        );
      }
      // Stimmung aus e.mood oder e.extendedProps.mood auslesen
      const eventMood = (e.mood !== undefined) ? e.mood : (e.extendedProps && e.extendedProps.mood ? e.extendedProps.mood : '');
      if (mood) {
        match = match && eventMood === mood;
      }
      // Kategorie aus e.category oder e.extendedProps.category auslesen
      const eventCategory = (e.category !== undefined) ? e.category : (e.extendedProps && e.extendedProps.category ? e.extendedProps.category : '');
      if (category) {
        match = match && eventCategory === category;
      }
      // Datum filtern
      if (startDate || endDate) {
        let entryDate = null;
        if (e.start) {
          entryDate = new Date(e.start);
        } else if (e.date) {
          entryDate = new Date(e.date);
        }
        if (entryDate) {
          if (startDate && entryDate < startDate) match = false;
          if (endDate && entryDate > endDate) match = false;
        }
      }
      return match;
    });
    renderResults(filtered);
  }

  // Zeigt die gefilterten Einträge als Liste an
  function renderResults(entries) {
    resultsList.innerHTML = '';
    // Scrollbar ab 10 Einträgen
    if (entries.length > 10) {
      resultsList.style.maxHeight = '340px';
      resultsList.style.overflowY = 'auto';
    } else {
      resultsList.style.maxHeight = '';
      resultsList.style.overflowY = '';
    }
    if (!entries.length) {
      resultsList.innerHTML = '<li class="list-group-item text-muted">Keine Treffer</li>';
      return;
    }
    entries.forEach(e => {
      const li = document.createElement('li');
      li.className = 'list-group-item d-flex align-items-center';
      li.setAttribute('data-id', e.id);
      li.innerHTML = `
        <span class="me-2">${e.start ? new Date(e.start).toLocaleDateString() : ''}</span>
        <span class="me-2">${e.title || ''}</span>
        <span class="me-2">${e.mood ? e.mood : ''}</span>
        ${e.has_attachment ? '<span title="Dateianhang"><i class="bi bi-paperclip"></i></span>' : ''}
      `;
      resultsList.appendChild(li);
    });
  }

  // Event-Handler für Filterfelder
  searchInput.addEventListener('input', filterEntries);
  moodSelect.addEventListener('change', filterEntries);
  categorySelect.addEventListener('change', filterEntries);
  if (startDateInput) startDateInput.addEventListener('change', filterEntries);
  if (endDateInput) endDateInput.addEventListener('change', filterEntries);
  // Zeigt initial alle Einträge
  filterEntries();

  // Export/Druck Buttons vorbereiten
  // PDF-Export: Erstellt eine PDF mit den gefilterten Einträgen (ohne Emojis)
  document.getElementById('orgaExportPdfBtn')?.addEventListener('click', function() {
    // PDF-Export mit jsPDF
    if (typeof window.jsPDF === 'undefined') {
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
      script.onload = exportOrgaResultsToPDF;
      document.body.appendChild(script);
    } else {
      exportOrgaResultsToPDF();
    }
  });

  // Hilfsfunktion für PDF-Export: Erstellt das PDF und entfernt Emojis
  function exportOrgaResultsToPDF() {
    const { jsPDF } = window.jspdf || window;
    const doc = new jsPDF();
    let y = 15;
    doc.setFontSize(16);
    doc.text('MoppDiary - Gefilterte Einträge', 10, y);
    y += 10;
    doc.setFontSize(11);
    const entries = Array.from(resultsList.querySelectorAll('li')).filter(li => !li.classList.contains('text-muted'));
    function removeEmojis(str) {
      // Entfernt Unicode-Emojis
      return str.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}\u{1FA70}-\u{1FAFF}\u{1F1E6}-\u{1F1FF}]/gu, '');
    }
    if (!entries.length) {
      doc.text('Keine Treffer', 10, y);
    } else {
      entries.forEach(li => {
        let text = li.innerText.replace(/\s+/g, ' ').trim();
        text = removeEmojis(text);
        doc.text(text, 10, y);
        y += 8;
        if (y > 280) {
          doc.addPage();
          y = 15;
        }
      });
    }
    doc.save('MoppDiary_Eintraege.pdf');
  }

  // CSV-Export: Erstellt eine CSV-Datei mit den gefilterten Einträgen inkl. Emojis
  document.getElementById('orgaExportCsvBtn')?.addEventListener('click', function() {
    // CSV-Export mit UTF-8 BOM für Excel
    const entries = Array.from(resultsList.querySelectorAll('li')).filter(li => !li.classList.contains('text-muted'));
    if (!entries.length) {
      alert('Keine Treffer zum Exportieren!');
      return;
    }
    // Spalten: Datum, Titel, Stimmung, Anhang
    let csv = 'Datum;Titel;Stimmung;Anhang\n';
    entries.forEach(li => {
      const date = li.querySelector('span.me-2:nth-child(1)')?.textContent.trim() || '';
      const title = li.querySelector('span.me-2:nth-child(2)')?.textContent.trim() || '';
      const mood = li.querySelector('span.me-2:nth-child(3)')?.textContent.trim() || '';
      const hasAttachment = li.querySelector('span[title="Dateianhang"]') ? 'Ja' : '';
      csv += `${date};${title};${mood};${hasAttachment}\n`;
    });
    // UTF-8 BOM hinzufügen (wichtig für Excel/Unicode)
    const BOM = '\uFEFF';
    const blob = new Blob([BOM + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'MoppDiary_Eintraege.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });

  // Print-Button: Zeigt nur die Trefferliste beim Drucken an (druckfreundliches Layout)
  document.getElementById('orgaPrintBtn')?.addEventListener('click', function() {
    // Druckfreundliches Layout aktivieren
    const orgaBox = document.getElementById('orgaBoxCard');
    if (!orgaBox) {
      window.print();
      return;
    }
    // CSS-Klasse für Druckansicht hinzufügen
    orgaBox.classList.add('print-only');
    document.body.classList.add('print-orgabox');
    // Nach dem Drucken Layout zurücksetzen
    window.onafterprint = function() {
      orgaBox.classList.remove('print-only');
      document.body.classList.remove('print-orgabox');
      window.onafterprint = null;
    };
    window.print();
  });
  // Export/Druck Buttons vorbereiten (nur Dummy-Handler)
  document.getElementById('orgaExportPdfBtn')?.addEventListener('click', function() {
    // PDF-Export mit jsPDF
    if (typeof window.jsPDF === 'undefined') {
      const script = document.createElement('script');
      script.src = 'https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js';
      script.onload = exportOrgaResultsToPDF;
      document.body.appendChild(script);
    } else {
      exportOrgaResultsToPDF();
    }
  });

  function exportOrgaResultsToPDF() {
    const { jsPDF } = window.jspdf || window;
    const doc = new jsPDF();
    let y = 15;
    doc.setFontSize(16);
    doc.text('MoppDiary - Gefilterte Einträge', 10, y);
    y += 10;
    doc.setFontSize(11);
    const entries = Array.from(resultsList.querySelectorAll('li')).filter(li => !li.classList.contains('text-muted'));
    function removeEmojis(str) {
      // Entfernt Unicode-Emojis
      return str.replace(/[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}\u{1F900}-\u{1F9FF}\u{1FA70}-\u{1FAFF}\u{1F1E6}-\u{1F1FF}]/gu, '');
    }
    if (!entries.length) {
      doc.text('Keine Treffer', 10, y);
    } else {
      entries.forEach(li => {
        let text = li.innerText.replace(/\s+/g, ' ').trim();
        text = removeEmojis(text);
        doc.text(text, 10, y);
        y += 8;
        if (y > 280) {
          doc.addPage();
          y = 15;
        }
      });
    }
    doc.save('MoppDiary_Eintraege.pdf');
  }
  };
  document.getElementById('orgaExportCsvBtn')?.addEventListener('click', function() {
    // CSV-Export
    const entries = Array.from(resultsList.querySelectorAll('li')).filter(li => !li.classList.contains('text-muted'));
    if (!entries.length) {
      alert('Keine Treffer zum Exportieren!');
      return;
    }
    // Spalten: Datum, Titel, Stimmung, Anhang
    let csv = 'Datum;Titel;Stimmung;Anhang\n';
    entries.forEach(li => {
      const date = li.querySelector('span.me-2:nth-child(1)')?.textContent.trim() || '';
      const title = li.querySelector('span.me-2:nth-child(2)')?.textContent.trim() || '';
      const mood = li.querySelector('span.me-2:nth-child(3)')?.textContent.trim() || '';
      const hasAttachment = li.querySelector('span[title="Dateianhang"]') ? 'Ja' : '';
      csv += `${date};${title};${mood};${hasAttachment}\n`;
    });
    // Download als Datei
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = 'MoppDiary_Eintraege.csv';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  });
  document.getElementById('orgaPrintBtn')?.addEventListener('click', function() {
    window.print();
  });

document.addEventListener('DOMContentLoaded', function() {
  const allDayCheckbox = document.getElementById('allDayCheckbox');
  const startTimeInput = document.getElementById('startTimeInput');
  const endTimeInput = document.getElementById('endTimeInput');
  const contentInput = document.querySelector('textarea[name="content"]');
  const peopleInput = document.querySelector('input[name="people"]');
  const moodSelect = document.querySelector('select[name="mood"]');
  const categorySelect = document.querySelector('select[name="category"]');
  // Korrigiert: Datei-Upload-Feld für 'attachments' (Mehrfach-Upload)
  const fileInput = document.querySelector('input[type="file"][name="attachments"]');
  function toggleFields() {
    const disabled = allDayCheckbox.checked;
    if (startTimeInput) {
      startTimeInput.disabled = disabled;
      if (disabled) {
        startTimeInput.value = '00:00'; // FullCalendar-Empfehlung für All-Day Start
      }
    }
    if (endTimeInput) {
      endTimeInput.disabled = disabled;
      if (disabled) {
        endTimeInput.value = '23:59'; // FullCalendar-Empfehlung für All-Day Ende
      }
    }
    if (contentInput) contentInput.disabled = disabled;
    if (peopleInput) peopleInput.disabled = disabled;
    if (moodSelect) moodSelect.disabled = disabled;
    if (categorySelect) categorySelect.disabled = disabled;
    if (fileInput) fileInput.disabled = disabled;
  }
  if (allDayCheckbox) {
    allDayCheckbox.addEventListener('change', toggleFields);
    toggleFields(); // Initialer Zustand
  }
});

