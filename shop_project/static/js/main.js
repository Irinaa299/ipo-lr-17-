// Функция загрузки товаров из API
// Функция загрузки товаров из API
async function loadProducts() {
    const productsGrid = document.getElementById('productsGrid');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const noProducts = document.getElementById('noProducts');
    
    if (!productsGrid) return; // Если мы не на странице каталога
    
    try {
        const response = await fetch('/api/products/');
        if (!response.ok) throw new Error('Ошибка загрузки');
        
        const data = await response.json();
        
        // API возвращает пагинированный ответ, товары в поле results
        const products = data.results || data;
        
        // Скрываем спиннер
        if (loadingSpinner) loadingSpinner.style.display = 'none';
        
        if (products.length === 0) {
            if (noProducts) noProducts.style.display = 'block';
            return;
        }
        
        // Показываем сетку товаров
        productsGrid.style.display = 'flex';
        productsGrid.innerHTML = '';
        
        // Создаем карточки товаров
        products.forEach(product => {
            const productCard = `
                <div class="col">
                    <div class="card h-100 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${product.title}</h5>
                            <p class="card-text text-muted">${product.description ? product.description.substring(0, 100) + '...' : 'Нет описания'}</p>
                            <p class="card-text">
                                <small class="text-muted">
                                    Категория: ${product.category_name || 'N/A'}<br>
                                    Бренд: ${product.manufacturer_name || 'N/A'}
                                </small>
                            </p>
                            <h4 class="text-primary">${product.price} руб.</h4>
                            <p class="card-text">
                                <small class="text-muted">Остаток: ${product.stock_quantity} шт.</small>
                            </p>
                            <a href="/catalog/${product.id}/" class="btn btn-outline-primary w-100">
                                Подробнее
                            </a>
                        </div>
                    </div>
                </div>
            `;
            productsGrid.innerHTML += productCard;
        });
        
    } catch (error) {
        console.error('Ошибка:', error);
        if (loadingSpinner) {
            loadingSpinner.innerHTML = '<p class="text-danger">Ошибка загрузки товаров</p>';
        }
    }
}

// Функция добавления в корзину
async function addToCart(productId) {
    try {
        const response = await fetch(`/api/cart/add/${productId}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        });
        
        if (response.ok) {
            // Показываем уведомление
            showNotification('Товар добавлен в корзину!', 'success');
        } else {
            showNotification('Ошибка при добавлении в корзину', 'error');
        }
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Ошибка соединения с сервером', 'error');
    }
}

// Получение CSRF токена
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Показ уведомления
function showNotification(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'success' ? 'success' : 'danger'} alert-dismissible fade show position-fixed`;
    alertDiv.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    document.body.appendChild(alertDiv);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
}

// Загружаем товары при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Если мы на странице каталога, загружаем товары
    if (document.getElementById('productsGrid')) {
        loadProducts();
    }
});