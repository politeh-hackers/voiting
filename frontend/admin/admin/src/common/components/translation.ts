import JSCookie from "@/common/utils/cookie";
import {Dropdown} from "@/site/components/dropdown";

const languages = {
    russian: 'ru',
    belarusian: 'be',
    chinese: 'zh-CN',
    us_and_a: 'en',
}
const allowedLanguages = [languages.russian, languages.belarusian, languages.chinese, languages.us_and_a]
const defaultLanguage = languages.russian;
const googleCookieTransName = 'googtrans'
const mainDomain = location.hostname.split('.').slice(-2);
let languageTitle = document.querySelector(".language-dropdown .dropdown-title")


export default function initTranslate(): void {
    let code: string = translateGetCode();
    if (code == 'CN') {
        code = 'zh-CN'
    }

    const dropdown = Dropdown.namedDropdowns;
    const languages = dropdown['languages'];

    languages.selectOptionByValue(code);

    languages.nullable = false;

    if (languages.selectedOption.value == 'be') {
        languageTitle.innerHTML = '<i class="flag-BY"></i><p>Белорусский</p>';
    } else if (languages.selectedOption.value == 'ru') {
        languageTitle.innerHTML = '<i class="flag-RU"></i><p>Русский</p>';
    } else if (languages.selectedOption.value == 'en') {
        languageTitle.innerHTML = '<i class="flag-US"></i><p>Английский</p>';
    } else if (languages.selectedOption.value == 'zh-CN') {
        languageTitle.innerHTML = '<i class="flag-CN"></i><p>Китайский</p>';
    }

    // No need to set same cookie again
    if (code === defaultLanguage) {
        translateClearCookie();
    }

    // Create translate element
    // @ts-ignore
    window.googleTranslateElementInit = () => {
        // @ts-ignore
        new google.translate.TranslateElement({
            autoDisplay: false,
            pageLanguage: defaultLanguage,
            layout: google.translate.TranslateElement.InlineLayout.SIMPLE,
        }, 'google_translate_element');
    };

    // Set new language
    languages.callBack = () => {
        const selectedLanguage = languages.selectedOption ? languages.selectedOption.value : '';
        if (selectedLanguage == 'ru' || selectedLanguage == null) {
            languageTitle.innerHTML = '<i class="flag-RU"></i> <p>Русский</p>';
        } else if (selectedLanguage == 'be') {
            languageTitle.innerHTML = '<i class="flag-BY"></i> <p>Белорусский</p>';
        } else if (selectedLanguage == 'en') {
            languageTitle.innerHTML = '<i class="flag-US"></i> <p>Английский</p>';
        } else if (selectedLanguage == 'zh-CN') {
            languageTitle.innerHTML = '<i class="flag-CN"></i> <p>Китайский</p>';
        }


        if (selectedLanguage && allowedLanguages.includes(selectedLanguage)) {
            translateSetCookie(selectedLanguage);
            window.location.reload();
        }
    }
}

function translateGetCode(): string {
    const currentLanguage = JSCookie.get(googleCookieTransName)
    const lang = (currentLanguage !== undefined && currentLanguage !== "null") ? currentLanguage : defaultLanguage;
    return lang.substr(-2);
}

function translateClearCookie(): void {
    JSCookie.set(googleCookieTransName, null);
    var myDate = new Date();
    myDate.setMonth(myDate.getMonth() + 12);
    document.cookie = googleCookieTransName + "=" + 'null' + ";expires=" + myDate
        + `;domain=.${mainDomain.join('.')};path=/`;
}

function translateSetCookie(code: string): void {
    JSCookie.set(googleCookieTransName, `/auto/${code}`);
    var myDate = new Date();
    myDate.setMonth(myDate.getMonth() + 12);
    document.cookie = googleCookieTransName + "=" + `/auto/${code}` + ";expires=" + myDate
        + `;domain=.${mainDomain.join('.')};path=/`;
}

