window.addEventListener('DOMContentLoaded', event => {
    // Activate SimpleLightbox plugin for portfolio items
    new SimpleLightbox({
        elements: '#portfolio a.portfolio-box'
    });
    // Custom JavaScript for nested dropdowns
    const dropdownSubmenus = document.querySelectorAll('.dropdown-submenu');

    dropdownSubmenus.forEach(function (submenu) {
        const dropdownToggle = submenu.querySelector('.dropdown-toggle');

        dropdownToggle.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();

            // Close other open submenus
            dropdownSubmenus.forEach(function (otherSubmenu) {
                if (otherSubmenu !== submenu) {
                    otherSubmenu.querySelector('.dropdown-menu').classList.remove('show');
                }
            });

            // Toggle the current submenu
            const dropdownMenu = submenu.querySelector('.dropdown-menu');
            dropdownMenu.classList.toggle('show');
        });
    });

    // Close dropdowns when clicking outside
    document.addEventListener('click', function () {
        dropdownSubmenus.forEach(function (submenu) {
            submenu.querySelector('.dropdown-menu').classList.remove('show');
        });
    });
});