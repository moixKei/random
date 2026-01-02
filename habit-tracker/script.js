document.addEventListener('DOMContentLoaded', () => {
    // Elementos del DOM
    const habitInput = document.getElementById('habitInput');
    const addHabitBtn = document.getElementById('addHabit');
    const habitList = document.getElementById('habitList');
    const completedCount = document.getElementById('completedCount');
    const totalCount = document.getElementById('totalCount');
    const streakCount = document.getElementById('streakCount');
    const resetWeekBtn = document.getElementById('resetWeek');
    const clearAllBtn = document.getElementById('clearAll');
    const weeklyProgress = document.getElementById('weeklyProgress');
    const progressPercent = document.getElementById('progressPercent');
    
    // Días de la semana
    const weekDays = ['L', 'M', 'X', 'J', 'V', 'S', 'D'];
    const dayCheckboxes = document.querySelectorAll('.day-checkbox input');
    
    // Inicializar hábitos desde localStorage o array vacío
    let habits = JSON.parse(localStorage.getItem('habits')) || [];
    let selectedDays = [true, true, true, true, true, true, true]; // Todos seleccionados por defecto
    
    // Cargar días seleccionados
    loadSelectedDays();
    
    // Actualizar estadísticas
    function updateStats() {
        const total = habits.length;
        const completed = habits.filter(habit => habit.done).length;
        const streak = calculateStreak();
        
        completedCount.textContent = completed;
        totalCount.textContent = total;
        streakCount.textContent = streak;
        
        // Actualizar barra de progreso
        const progress = total > 0 ? Math.round((completed / total) * 100) : 0;
        weeklyProgress.style.width = `${progress}%`;
        progressPercent.textContent = `${progress}%`;
    }
    
    // Calcular la racha actual
    function calculateStreak() {
        if (habits.length === 0) return 0;
        
        // Simulación: para una demo, calculamos la racha como el número de hábitos completados hoy
        const today = new Date().toLocaleDateString();
        const todayCompleted = habits.filter(habit => 
            habit.lastCompleted === today
        ).length;
        
        return todayCompleted > 0 ? Math.min(todayCompleted, 7) : 0;
    }
    
    // Guardar hábitos en localStorage
    function saveHabits() {
        localStorage.setItem('habits', JSON.stringify(habits));
        updateStats();
    }
    
    // Guardar días seleccionados
    function saveSelectedDays() {
        localStorage.setItem('selectedDays', JSON.stringify(selectedDays));
    }
    
    // Cargar días seleccionados
    function loadSelectedDays() {
        const savedDays = JSON.parse(localStorage.getItem('selectedDays'));
        if (savedDays) {
            selectedDays = savedDays;
            dayCheckboxes.forEach((checkbox, index) => {
                checkbox.checked = selectedDays[index];
            });
        }
    }
    
    // Renderizar lista de hábitos
    function renderHabits() {
        habitList.innerHTML = '';
        
        if (habits.length === 0) {
            habitList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-clipboard-list fa-3x"></i>
                    <p>No tienes hábitos todavía. ¡Añade uno para empezar!</p>
                </div>
            `;
            return;
        }
        
        habits.forEach((habit, index) => {
            const li = document.createElement('li');
            li.className = 'habit-item';
            
            // Crear indicadores de días
            const dayIndicators = weekDays.map((day, dayIndex) => {
                const isActive = habit.days ? habit.days[dayIndex] : selectedDays[dayIndex];
                return `
                    <div class="day-indicator ${isActive ? 'active' : 'inactive'}">
                        ${day}
                    </div>
                `;
            }).join('');
            
            li.innerHTML = `
                <div class="habit-content">
                    <input type="checkbox" class="habit-checkbox" ${habit.done ? 'checked' : ''}>
                    <span class="habit-name ${habit.done ? 'completed' : ''}">${habit.name}</span>
                    <div class="habit-days">
                        ${dayIndicators}
                    </div>
                </div>
                <div class="habit-actions">
                    <button class="btn-icon btn-edit" title="Editar hábito">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-icon btn-delete" title="Eliminar hábito">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            `;
            
            // Eventos para el checkbox
            const checkbox = li.querySelector('.habit-checkbox');
            checkbox.addEventListener('change', () => {
                habits[index].done = !habits[index].done;
                
                // Si se marca como completado, guardar la fecha
                if (habits[index].done) {
                    habits[index].lastCompleted = new Date().toLocaleDateString();
                }
                
                saveHabits();
                renderHabits();
            });
            
            // Evento para editar
            const editBtn = li.querySelector('.btn-edit');
            editBtn.addEventListener('click', () => {
                editHabit(index);
            });
            
            // Evento para eliminar
            const deleteBtn = li.querySelector('.btn-delete');
            deleteBtn.addEventListener('click', () => {
                deleteHabit(index);
            });
            
            habitList.appendChild(li);
        });
    }
    
    // Añadir nuevo hábito
    function addHabit() {
        const name = habitInput.value.trim();
        if (name === '') {
            showNotification('Por favor, escribe un nombre para el hábito', 'warning');
            return;
        }
        
        const newHabit = {
            id: Date.now(),
            name: name,
            done: false,
            days: [...selectedDays], // Copiar los días seleccionados
            createdAt: new Date().toISOString(),
            lastCompleted: null
        };
        
        habits.push(newHabit);
        habitInput.value = '';
        saveHabits();
        renderHabits();
        showNotification(`¡Hábito "${name}" añadido!`, 'success');
    }
    
    // Editar hábito existente
    function editHabit(index) {
        const habit = habits[index];
        const newName = prompt('Editar nombre del hábito:', habit.name);
        
        if (newName && newName.trim() !== '') {
            habits[index].name = newName.trim();
            saveHabits();
            renderHabits();
            showNotification('Hábito actualizado correctamente', 'info');
        }
    }
    
    // Eliminar hábito
    function deleteHabit(index) {
        if (confirm(`¿Seguro que quieres eliminar el hábito "${habits[index].name}"?`)) {
            const deletedHabit = habits.splice(index, 1)[0];
            saveHabits();
            renderHabits();
            showNotification(`Hábito "${deletedHabit.name}" eliminado`, 'error');
        }
    }
    
    // Reiniciar semana (marcar todos como no completados)
    function resetWeek() {
        if (habits.length === 0) {
            showNotification('No hay hábitos para reiniciar', 'warning');
            return;
        }
        
        if (confirm('¿Reiniciar todos los hábitos para la nueva semana?')) {
            habits.forEach(habit => {
                habit.done = false;
            });
            saveHabits();
            renderHabits();
            showNotification('¡Semana reiniciada! Todos los hábitos están listos.', 'success');
        }
    }
    
    // Eliminar todos los hábitos
    function clearAllHabits() {
        if (habits.length === 0) {
            showNotification('No hay hábitos para eliminar', 'warning');
            return;
        }
        
        if (confirm('¿Seguro que quieres eliminar TODOS los hábitos? Esta acción no se puede deshacer.')) {
            habits = [];
            saveHabits();
            renderHabits();
            showNotification('Todos los hábitos han sido eliminados', 'error');
        }
    }
    
    // Mostrar notificación temporal
    function showNotification(message, type) {
        // Eliminar notificación anterior si existe
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }
        
        // Crear nueva notificación
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <span>${message}</span>
            <button class="notification-close">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        document.body.appendChild(notification);
        
        // Mostrar con animación
        setTimeout(() => {
            notification.classList.add('show');
        }, 10);
        
        // Cerrar notificación al hacer clic en la X
        const closeBtn = notification.querySelector('.notification-close');
        closeBtn.addEventListener('click', () => {
            notification.classList.remove('show');
            setTimeout(() => {
                notification.remove();
            }, 300);
        });
        
        // Ocultar automáticamente después de 4 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.classList.remove('show');
                setTimeout(() => {
                    notification.remove();
                }, 300);
            }
        }, 4000);
    }
    
    // Actualizar días seleccionados
    dayCheckboxes.forEach((checkbox, index) => {
        checkbox.addEventListener('change', () => {
            selectedDays[index] = checkbox.checked;
            saveSelectedDays();
        });
    });
    
    // Event Listeners
    addHabitBtn.addEventListener('click', addHabit);
    habitInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addHabit();
        }
    });
    resetWeekBtn.addEventListener('click', resetWeek);
    clearAllBtn.addEventListener('click', clearAllHabits);
    
    // Inicializar
    renderHabits();
    updateStats();
});

// Añadir estilos para notificaciones
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background-color: white;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
        z-index: 1000;
        transform: translateX(120%);
        transition: transform 0.3s ease;
        max-width: 350px;
        border-left: 5px solid #3498db;
    }
    
    .notification.show {
        transform: translateX(0);
    }
    
    .notification.success {
        border-left-color: #2ecc71;
    }
    
    .notification.error {
        border-left-color: #e74c3c;
    }
    
    .notification.warning {
        border-left-color: #f39c12;
    }
    
    .notification.info {
        border-left-color: #3498db;
    }
    
    .notification-close {
        background: none;
        border: none;
        cursor: pointer;
        color: #7f8c8d;
        font-size: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: #7f8c8d;
    }
    
    .empty-state i {
        margin-bottom: 15px;
        color: #bdc3c7;
    }
`;
document.head.appendChild(style);