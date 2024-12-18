import priorityNav from "priority-nav"

export default function initBurger() {
    const hamb = <HTMLElement>document.querySelector("#hamb");
    const popup = <HTMLElement>document.querySelector("#popup");
    const search = <HTMLElement>document.querySelector("#header-block__search");
    const search_input = <HTMLElement>document.getElementById('header__input');
    const net_links = <HTMLElement>document.querySelector("#social-network-links");
    const body = <HTMLElement>document.body;
    const menu = <HTMLElement>document.querySelector("#menu").cloneNode(true);
    const closeableBannerElement = <HTMLElement>document.getElementById("closeable-banner");


    if (hamb && popup && search && search_input && net_links && body && menu) {
        const renderPopup = () => {
            popup.appendChild(menu);
        };

        hamb.addEventListener("click", (e) => {
            e.preventDefault();
            popup.classList.toggle("open");
            hamb.classList.toggle("active");
            body.classList.toggle("noscroll");
            search.classList.toggle("open");
            net_links.classList.toggle("open");
            window.scrollTo(0, 0);

            const cookieString = document.cookie;
            const cookieNameIndex = cookieString.indexOf(`DISABLE_BANNER_IN_MENU=`);

            if (closeableBannerElement) {
                if (cookieNameIndex === -1) {
                    closeableBannerElement.style.display = closeableBannerElement.style.display === "none" ? "flex" : "none";
                }
            }


            renderPopup();

            let headerOpenDropdown = document.querySelectorAll(".open-mobile-dropdown");

            if (headerOpenDropdown[1]) {
                headerOpenDropdown[1].addEventListener("click", () => {
                    let dropdownContent = document.querySelectorAll(".dropdown-content")
                    dropdownContent[1].classList.toggle("open")
                })
            }
        });

        Array.from(menu.children).slice(0, -1).forEach((element) => {
            element.addEventListener("click", () => {
                popup.classList.remove("open");
                hamb.classList.remove("active");
                body.classList.remove("noscroll");
                search.classList.remove("open");
                net_links.classList.remove("open");
            });
        });

        search_input.addEventListener('focus', () => {
            search.style.border = '1px solid var(--primary-color)';
        });

        search_input.addEventListener('blur', () => {
            search.style.border = 'solid 1px #CECECE';
        });
    }

    if (closeableBannerElement) {
        body.style.gridTemplateRows = "min-content min-content auto min-content"
    } else {
        body.style.gridTemplateRows = "min-content auto min-content"
    }

    if (closeableBannerElement) {
        const closeable_banner = <HTMLElement>document.getElementById('cl-banner-btn');
        body.style.gridTemplateRows = "min-content min-content auto min-content"
        if (closeable_banner) {
            closeable_banner.addEventListener("click", () => {
                document.cookie = "DISABLE_BANNER_IN_MENU=yes;path=/"
                document.getElementById("closeable-banner").style.display = "none";
                body.style.gridTemplateRows = "min-content auto min-content"
                withoutBanner();
                document.body.style.paddingTop = `${headerY.height}px`;
                scrolledHeader();
                main.style.marginTop = "0";
                closeableBannerElement.classList.add("closed")
            });
        }
    }


}

const header = <HTMLElement>document.getElementsByTagName('header')[0];
const main = <HTMLElement>document.getElementsByTagName('main')[0];
const closeableBannerElement = <HTMLElement>document.getElementById("closeable-banner");
const headerY = header.getBoundingClientRect();

var upButton = document.createElement('div');

document.addEventListener('DOMContentLoaded', function () {
    withoutBanner();
    createUpButton();
});

window.addEventListener('scroll', function () {

    scrolledHeader();

    if (window.scrollY > 1300) {
        upButton.style.visibility = 'visible';
        upButton.style.opacity = '1';
    } else {
        upButton.style.opacity = '0';
        upButton.style.visibility = 'hidden';
    }

});

function scrolledHeader() {
    if (header && closeableBannerElement) {

        let cb = closeableBannerElement.getBoundingClientRect();

        if (cb.bottom <= 0) {
            header.classList.add("scrolled");
            if (closeableBannerElement.classList.contains("closed")) {
                main.style.marginTop = "0";
            } else {
                main.style.marginTop = "116px";
            }
        } else if (cb.bottom > 0) {
            header.classList.remove("scrolled");
            main.style.marginTop = "0";
        }
    }
}

function withoutBanner() {
    if (!closeableBannerElement && header) {
        header.classList.add("scrolled");
        document.body.style.paddingTop = `${headerY.height}px`;
        main.style.marginTop = "0";
    }
}

function createUpButton() {

    upButton.classList.add("up-button");
    let icon = document.createElement('i');
    icon.classList.add('fa', 'fa-arrow-up');
    upButton.appendChild(icon);

    upButton.addEventListener("click", () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });

    main.appendChild(upButton);
}


let nav = priorityNav.init({
    initClass: "js-priorityNav", // Class that will be printed on html element to allow conditional css styling.
    mainNavWrapper: ".header-block__navbar__wrap", // mainnav wrapper selector (must be direct parent from mainNav)
    mainNav: ".menu", // mainnav selector. (must be inline-block)
    navDropdownClassName: "header-show-more-dropdown", // class used for the dropdown - this is a class name, not a selector.
    navDropdownToggleClassName: "header-show-more", // class used for the dropdown toggle - this is a class name, not a selector.
    navDropdownLabel: "Дополнительно...", // Text that is used for the dropdown toggle.
    navDropdownBreakpointLabel: "Дополнительно...", //button label for navDropdownToggle when the breakPoint is reached.
    breakPoint: 0, //amount of pixels when all menu items should be moved to dropdown to simulate a mobile menu
    throttleDelay: 150, // this will throttle the calculating logic on resize because i'm a responsible dev.
    offsetPixels: 0, // increase to decrease the time it takes to move an item.
});

