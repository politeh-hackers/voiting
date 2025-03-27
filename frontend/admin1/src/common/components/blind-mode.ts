import JSCookie from "@/common/utils/cookie";

const blindModeCookieName = 'blindMode'
const blindModeButton = document.querySelector(".blind-mode-button");
const body = document.body;
const blindModeOffText = 'Обычная версия';
const blindModeOnText = 'Версия для слабовидящих';
const mainDomain = location.hostname.split('.').slice(-2);


export default function initializeBlindMode() {
    const isBlindMode = JSCookie.get(blindModeCookieName);

    if (blindModeButton) {
        blindModeButton.addEventListener("click", toggleBlindMode);
    }

    // Initialize blind mode based on the cookie
    isBlindMode ? setBlindMode() : removeBlindMode();
}

function toggleBlindMode() {
    const isBlindMode = JSCookie.get(blindModeCookieName);
    if (isBlindMode) {
        JSCookie.remove(blindModeCookieName, {domain: `.${mainDomain.join('.')}`});
        removeBlindMode();
    } else {
        JSCookie.set(blindModeCookieName, 'true', {domain: `.${mainDomain.join('.')}`});
        setBlindMode();
    }
}

function setBlindMode() {
    body.classList.toggle('blind-mode');
    blindModeButton.innerHTML = `<i class="far fa-glasses"></i>  ${blindModeOffText}`;
}

function removeBlindMode() {
    body.classList.remove('blind-mode');
    blindModeButton.innerHTML = `<i class='far fa-glasses'></i> ${blindModeOnText}`;
}
