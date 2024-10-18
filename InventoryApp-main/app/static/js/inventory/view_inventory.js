const searchInput = document.getElementById('searchInput');
const filterForm = document.getElementById('filterForm');
let searchTimeout;

searchInput.addEventListener('input', function() {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
        filterForm.submit();
    }, 500); // Wait for 500ms after the user stops typing
});



document.addEventListener('DOMContentLoaded', function() {
    const printInventoryBtn = document.getElementById('printInventory');
    const printQRCodesBtn = document.getElementById('printQRCodes');

    if (printInventoryBtn) {
        printInventoryBtn.addEventListener('click', function() {
            var currentUrl = new URL(window.location.href);
            var printUrl = "/inventory/print_inventory?" + currentUrl.searchParams.toString();
            window.open(printUrl, '_blank');
        });
    }

    if (printQRCodesBtn) {
        printQRCodesBtn.addEventListener('click', function() {
            window.location.href = '/inventory/select_qr_codes';
        });
    }
});