document.addEventListener('DOMContentLoaded', () => {
  const calendar = document.getElementById('calendar');
  const noteModal = document.getElementById('noteModal');
  const noteText = document.getElementById('noteText');
  const saveNoteBtn = document.getElementById('saveNote');
  const deleteNoteBtn = document.getElementById('deleteNote');
  const closeModalBtn = document.getElementById('closeModal');
  const modalOverlay = document.getElementById('modalOverlay');
  const tagModal = document.getElementById('tagModal');
  const tagNameInput = document.getElementById('tagName');
  const saveTagBtn = document.getElementById('saveTag');
  const closeTagModalBtn = document.getElementById('closeTagModal');
  const currentMonthElement = document.getElementById('currentMonth');
  const searchNotesInput = document.getElementById('searchNotes');
  const clearSearchBtn = document.getElementById('clearSearch');
  const exportNotesBtn = document.getElementById('exportNotes');
  const importNotesBtn = document.getElementById('importNotes');
  const importFileInput = document.getElementById('importFile');
  const todayBtn = document.getElementById('todayBtn');
  const addTagBtn = document.getElementById('addTagBtn');
  const newTagBtn = document.getElementById('newTagBtn');
  const noteTagSelect = document.getElementById('noteTag');
  const tagsList = document.getElementById('tagsList');
  const monthSummary = document.getElementById('monthSummary');
  const totalNotesElement = document.getElementById('totalNotes');
  const daysWithNotesElement = document.getElementById('daysWithNotes');
  const tagCountElement = document.getElementById('tagCount');

  const prevMonthBtn = document.getElementById('prevMonth');
  const nextMonthBtn = document.getElementById('nextMonth');
  const prevYearBtn = document.getElementById('prevYear');
  const nextYearBtn = document.getElementById('nextYear');

  let selectedDate = null;
  let currentDate = new Date();
  let notes = JSON.parse(localStorage.getItem('notes')) || {};
  let tags = JSON.parse(localStorage.getItem('tags')) || {};
  let searchQuery = '';
  let selectedTagColor = '#FF6B6B';

  const tagColors = [
    '#FF6B6B', '#4ECDC4', '#FFD166', '#06D6A0', '#118AB2', '#9D4EDD',
    '#FF9A76', '#A3DE83', '#FF8A5C', '#00BBF9', '#F15BB5', '#9B5DE5'
  ];

  if (Object.keys(tags).length === 0) {
    tags = {
      trabajo: { name: 'Trabajo', color: '#FF6B6B' },
      personal: { name: 'Personal', color: '#4ECDC4' },
      ideas: { name: 'Ideas', color: '#FFD166' },
      importante: { name: 'Importante', color: '#06D6A0' }
    };
    saveTags();
  }

  function saveNotes() {
    localStorage.setItem('notes', JSON.stringify(notes));
    updateStats();
    updateMonthSummary();
  }

  function saveTags() {
    localStorage.setItem('tags', JSON.stringify(tags));
    renderTagList();
    updateTagSelect();
    updateStats();
  }

  function updateStats() {
    const noteEntries = Object.entries(notes);
    const totalNotes = noteEntries.length;
    const daysWithNotes = new Set(noteEntries.map(([date]) => date.split('T')[0])).size;
    const tagCount = Object.keys(tags).length;

    totalNotesElement.textContent = totalNotes;
    daysWithNotesElement.textContent = daysWithNotes;
    tagCountElement.textContent = tagCount;
  }

  function renderCalendar() {
    calendar.innerHTML = '';
    
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    
    const monthNames = [
      'Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio',
      'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'
    ];
    currentMonthElement.textContent = `${monthNames[month]} ${year}`;
    
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);
    const daysInMonth = lastDay.getDate();
    const startingDay = firstDay.getDay() === 0 ? 6 : firstDay.getDay() - 1;
    
    const prevMonthLastDay = new Date(year, month, 0).getDate();
    for (let i = 0; i < startingDay; i++) {
      const day = document.createElement('div');
      day.className = 'day other-month';
      const dayNumber = prevMonthLastDay - startingDay + i + 1;
      day.innerHTML = `<div class="day-number">${dayNumber}</div>`;
      calendar.appendChild(day);
    }
    
    const today = new Date();
    const isCurrentMonth = today.getMonth() === month && today.getFullYear() === year;
    
    for (let i = 1; i <= daysInMonth; i++) {
      const day = document.createElement('div');
      day.className = 'day';
      
      const date = new Date(year, month, i);
      const dateKey = date.toISOString().split('T')[0];
      const dayNotes = notes[dateKey];
      
      if (isCurrentMonth && i === today.getDate()) {
        day.classList.add('current-day');
      }
      
      if (dayNotes) {
        day.classList.add('has-notes');
        
        if (dayNotes.tag && tags[dayNotes.tag]) {
          const tagColor = tags[dayNotes.tag].color;
          day.innerHTML += `<div class="day-tag" style="background-color: ${tagColor}"></div>`;
        }
        
        const preview = dayNotes.text.replace(/<[^>]*>/g, '').substring(0, 50);
        day.innerHTML += `<div class="day-notes-preview">${preview}${preview.length >= 50 ? '...' : ''}</div>`;
      }
      
      day.innerHTML = `<div class="day-number">${i}</div>` + (day.innerHTML || '');
      
      day.addEventListener('click', () => openNoteModal(dateKey, i));
      
      if (searchQuery && dayNotes && 
          dayNotes.text.toLowerCase().includes(searchQuery.toLowerCase())) {
        day.style.boxShadow = '0 0 0 3px #FFD166';
      }
      
      calendar.appendChild(day);
    }

    const totalCells = 42;
    const remainingCells = totalCells - (startingDay + daysInMonth);
    for (let i = 1; i <= remainingCells; i++) {
      const day = document.createElement('div');
      day.className = 'day other-month';
      day.innerHTML = `<div class="day-number">${i}</div>`;
      calendar.appendChild(day);
    }
  }

  function openNoteModal(dateKey, dayNumber) {
    selectedDate = dateKey;
    
    const date = new Date(dateKey);
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    const modalDateElement = document.getElementById('modalDate');
    modalDateElement.textContent = date.toLocaleDateString('es-ES', options);
    
    const note = notes[dateKey];
    noteText.innerHTML = note ? note.text : '';
    
    noteTagSelect.value = note ? note.tag || '' : '';
    
    deleteNoteBtn.style.display = note ? 'flex' : 'none';
    
    noteModal.classList.remove('hidden');
    modalOverlay.classList.remove('hidden');
    
    setTimeout(() => noteText.focus(), 100);
  }

  function closeNoteModal() {
    noteModal.classList.add('hidden');
    modalOverlay.classList.add('hidden');
    selectedDate = null;
  }

  function saveNote() {
    if (!selectedDate) return;
    
    const text = noteText.innerHTML.trim();
    const tag = noteTagSelect.value;
    
    if (text === '') {
      if (notes[selectedDate]) {
        delete notes[selectedDate];
        saveNotes();
      }
    } else {
      notes[selectedDate] = {
        text: text,
        tag: tag,
        updated: new Date().toISOString()
      };
      saveNotes();
    }
    
    renderCalendar();
    closeNoteModal();
  }

  function deleteNote() {
    if (!selectedDate || !confirm('¿Eliminar esta nota?')) return;
    
    delete notes[selectedDate];
    saveNotes();
    renderCalendar();
    closeNoteModal();
  }

  function renderTagList() {
    tagsList.innerHTML = '';
    
    const tagCounts = {};
    Object.values(notes).forEach(note => {
      if (note.tag) {
        tagCounts[note.tag] = (tagCounts[note.tag] || 0) + 1;
      }
    });
    
    Object.entries(tags).forEach(([id, tag]) => {
      const tagElement = document.createElement('div');
      tagElement.className = 'tag-item';
      tagElement.innerHTML = `
        <div class="tag-color" style="background-color: ${tag.color}"></div>
        <div class="tag-name">${tag.name}</div>
        <div class="tag-count">${tagCounts[id] || 0}</div>
      `;
      
      tagElement.addEventListener('click', () => {
        searchNotesInput.value = '';
        searchQuery = '';
        clearSearchBtn.classList.add('hidden');
        
        const filteredNotes = {};
        Object.entries(notes).forEach(([date, note]) => {
          if (note.tag === id) {
            filteredNotes[date] = note;
          }
        });
        
        document.querySelectorAll('.day').forEach(day => {
          const dayNumber = parseInt(day.querySelector('.day-number').textContent);
          if (!isNaN(dayNumber)) {
            const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayNumber);
            const dateKey = date.toISOString().split('T')[0];
            if (filteredNotes[dateKey]) {
              day.style.boxShadow = '0 0 0 3px ' + tag.color;
            } else {
              day.style.boxShadow = '';
            }
          }
        });
      });
      
      tagsList.appendChild(tagElement);
    });
  }

  function updateTagSelect() {
    noteTagSelect.innerHTML = '<option value="">Sin etiqueta</option>';
    
    Object.entries(tags).forEach(([id, tag]) => {
      const option = document.createElement('option');
      option.value = id;
      option.textContent = tag.name;
      noteTagSelect.appendChild(option);
    });
  }

  function updateMonthSummary() {
    monthSummary.innerHTML = '';
    
    const year = currentDate.getFullYear();
    const month = currentDate.getMonth();
    const monthNotes = [];
    
    Object.entries(notes).forEach(([dateKey, note]) => {
      const date = new Date(dateKey);
      if (date.getFullYear() === year && date.getMonth() === month) {
        monthNotes.push({
          date: dateKey,
          day: date.getDate(),
          ...note
        });
      }
    });
    
    monthNotes.sort((a, b) => a.day - b.day);
    
    if (monthNotes.length === 0) {
      monthSummary.innerHTML = '<p class="empty-summary">No hay notas este mes</p>';
      return;
    }
    
    monthNotes.forEach(note => {
      const summaryItem = document.createElement('div');
      summaryItem.className = 'summary-item';
      
      const preview = note.text.replace(/<[^>]*>/g, '').substring(0, 40);
      const tagBadge = note.tag ? 
        `<span style="color: ${tags[note.tag].color}; font-weight: bold;">[${tags[note.tag].name}]</span> ` : '';
      
      summaryItem.innerHTML = `
        <div class="summary-date">${note.day}</div>
        <div class="summary-preview">${tagBadge}${preview}${preview.length >= 40 ? '...' : ''}</div>
      `;
      
      summaryItem.addEventListener('click', () => {
        openNoteModal(note.date, note.day);
      });
      
      monthSummary.appendChild(summaryItem);
    });
  }

  searchNotesInput.addEventListener('input', (e) => {
    searchQuery = e.target.value.trim();
    
    if (searchQuery) {
      clearSearchBtn.classList.remove('hidden');
      
      document.querySelectorAll('.day').forEach(day => {
        const dayNumber = parseInt(day.querySelector('.day-number').textContent);
        if (!isNaN(dayNumber)) {
          const date = new Date(currentDate.getFullYear(), currentDate.getMonth(), dayNumber);
          const dateKey = date.toISOString().split('T')[0];
          const note = notes[dateKey];
          
          if (note && note.text.toLowerCase().includes(searchQuery.toLowerCase())) {
            day.style.boxShadow = '0 0 0 3px #FFD166';
          } else {
            day.style.boxShadow = '';
          }
        }
      });
    } else {
      clearSearchBtn.classList.add('hidden');
      document.querySelectorAll('.day').forEach(day => {
        day.style.boxShadow = '';
      });
    }
  });

  clearSearchBtn.addEventListener('click', () => {
    searchNotesInput.value = '';
    searchQuery = '';
    clearSearchBtn.classList.add('hidden');
    
    document.querySelectorAll('.day').forEach(day => {
      day.style.boxShadow = '';
    });
  });

  exportNotesBtn.addEventListener('click', () => {
    const dataStr = JSON.stringify({ notes, tags }, null, 2);
    const dataUri = 'data:application/json;charset=utf-8,'+ encodeURIComponent(dataStr);
    
    const exportFileDefaultName = `notas-${new Date().toISOString().split('T')[0]}.json`;
    
    const linkElement = document.createElement('a');
    linkElement.setAttribute('href', dataUri);
    linkElement.setAttribute('download', exportFileDefaultName);
    linkElement.click();
    
    alert('Notas exportadas correctamente');
  });

  importNotesBtn.addEventListener('click', () => {
    importFileInput.click();
  });

  importFileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (!file) return;
    
    if (confirm('¿Importar notas? Se sobrescribirán las notas actuales.')) {
      const reader = new FileReader();
      reader.onload = (event) => {
        try {
          const data = JSON.parse(event.target.result);
          notes = data.notes || {};
          tags = data.tags || {};
          saveNotes();
          saveTags();
          renderCalendar();
          alert('Notas importadas correctamente');
        } catch (error) {
          alert('Error al importar el archivo');
        }
      };
      reader.readAsText(file);
    }
    
    importFileInput.value = '';
  });

  prevMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() - 1);
    renderCalendar();
    updateMonthSummary();
  });

  nextMonthBtn.addEventListener('click', () => {
    currentDate.setMonth(currentDate.getMonth() + 1);
    renderCalendar();
    updateMonthSummary();
  });

  prevYearBtn.addEventListener('click', () => {
    currentDate.setFullYear(currentDate.getFullYear() - 1);
    renderCalendar();
    updateMonthSummary();
  });

  nextYearBtn.addEventListener('click', () => {
    currentDate.setFullYear(currentDate.getFullYear() + 1);
    renderCalendar();
    updateMonthSummary();
  });

  todayBtn.addEventListener('click', () => {
    currentDate = new Date();
    renderCalendar();
    updateMonthSummary();
  });

  document.querySelectorAll('.format-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const command = btn.dataset.command;
      const value = btn.dataset.value;
      
      document.execCommand(command, false, value);
      noteText.focus();
    });
  });

  addTagBtn.addEventListener('click', () => {
    tagModal.classList.remove('hidden');
    modalOverlay.classList.remove('hidden');
    tagNameInput.value = '';
    
    document.querySelectorAll('.color-option').forEach(option => {
      option.classList.remove('selected');
    });
    document.querySelector('.color-option').classList.add('selected');
    selectedTagColor = tagColors[0];
  });

  newTagBtn.addEventListener('click', () => {
    addTagBtn.click();
  });

  document.querySelectorAll('.color-option').forEach((option, index) => {
    option.addEventListener('click', () => {
      document.querySelectorAll('.color-option').forEach(opt => {
        opt.classList.remove('selected');
      });
      option.classList.add('selected');
      selectedTagColor = tagColors[index];
    });
  });

  saveTagBtn.addEventListener('click', () => {
    const tagName = tagNameInput.value.trim();
    if (!tagName) {
      alert('Por favor ingresa un nombre para la etiqueta');
      return;
    }
    
    const tagId = tagName.toLowerCase().replace(/\s+/g, '_');
    
    if (tags[tagId]) {
      alert('Ya existe una etiqueta con ese nombre');
      return;
    }
    
    tags[tagId] = {
      name: tagName,
      color: selectedTagColor
    };
    
    saveTags();
    closeTagModal();
  });

  function closeTagModal() {
    tagModal.classList.add('hidden');
    modalOverlay.classList.add('hidden');
  }

  saveNoteBtn.addEventListener('click', saveNote);
  deleteNoteBtn.addEventListener('click', deleteNote);
  closeModalBtn.addEventListener('click', closeNoteModal);
  closeTagModalBtn.addEventListener('click', closeTagModal);
  modalOverlay.addEventListener('click', () => {
    closeNoteModal();
    closeTagModal();
  });

  renderCalendar();
  renderTagList();
  updateTagSelect();
  updateMonthSummary();
  updateStats();
});