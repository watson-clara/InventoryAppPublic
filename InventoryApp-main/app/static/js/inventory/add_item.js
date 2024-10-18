document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addItemForm');
    const quantityInput = document.getElementById('quantity');
    const minQuantityInput = document.getElementById('minimum_quantity');
    const maxQuantityInput = document.getElementById('max_quantity');

    function updateStockStatus() {
        const quantity = parseInt(quantityInput.value) || 0;
        const minQuantity = parseInt(minQuantityInput.value) || 0;
        const maxQuantity = parseInt(maxQuantityInput.value) || 0;

        if (quantity <= minQuantity) {
            stockStatusInput.value = 'out of stock';
        } else if (quantity < maxQuantity) {
            stockStatusInput.value = 'low stock';
        } else {
            stockStatusInput.value = 'in stock';
        }
    }

    quantityInput.addEventListener('input', updateStockStatus);
    minQuantityInput.addEventListener('input', updateStockStatus);
    maxQuantityInput.addEventListener('input', updateStockStatus);

    form.addEventListener('submit', function(event) {
        updateStockStatus();
    });
});