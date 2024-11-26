import Swiper, {Navigation} from "swiper";
import {gradientUtils} from "@/site/components/utils";


export default function initSwipers() {
    const swiperGradient = <HTMLDivElement>document.querySelector('.swiper .shadow-gradient');
    const swiperBandGradient = <HTMLDivElement>document.querySelector('.swiper-band .shadow-gradient');
    const swiperPartnerGradient = <HTMLDivElement>document.querySelector('.swiper-partner .shadow-gradient');


    if (document.querySelector('.product-swiper')) {
        new Swiper(".product-swiper", {
            modules:[Navigation],
            slidesPerView: 'auto',
            spaceBetween: 13,
            navigation: {
                nextEl: ".product-swiper__block .next",
                prevEl: ".product-swiper__block .prev",
            }
        });
    }

    if (document.querySelector('.service-swiper')) {
        new Swiper(".service-swiper", {
            modules:[Navigation],
            slidesPerView: 'auto',
            spaceBetween: 13,
            navigation: {
                nextEl: ".service-swiper__block .next",
                prevEl: ".service-swiper__block .prev",
            }
        });
    }

    if (document.querySelector('.poster-block-items')) {
        new Swiper(".poster-block-items", {
            modules:[Navigation],
            slidesPerView: 'auto',
            spaceBetween: 13,
            navigation: {
                nextEl: ".pb-r",
                prevEl: ".pb-l",
            },
            on: {
                init(sw) {
                    sw.updateSlides();
                    if (sw.slides.length < 2) {
                        if (swiperGradient) {
                            swiperGradient.classList.add('off');
                        }
                    }
                },
                ...gradientUtils(swiperGradient)
            }
        });
    }
    if (document.querySelector('.swiper-band')) {
        new Swiper(".swiper-band", {
            modules:[Navigation],
            slidesPerView: 'auto',
            spaceBetween: 13,
            navigation: {
                nextEl: ".bb-r",
                prevEl: ".bb-l",
            },
            on: {
                init(sw) {
                    if (sw.params.slidesPerView >= sw.slides.length || sw.slides.length < 2) {
                        if (swiperBandGradient) {
                            swiperBandGradient.classList.add('off');
                        }
                    }
                },
                ...gradientUtils(swiperBandGradient)
            }
        });
    }


    if (document.querySelector('.swiper-partner')) {
        new Swiper(".swiper-partner", {
             modules:[Navigation],
            slidesPerView: "auto",
            loop: false,
            spaceBetween: 14,
            breakpoints:{
                401: {
                    slidesPerView: "auto",
                },
                1: {
                    slidesPerView: 1,
                }
            },
            navigation: {
                nextEl: ".par-r",
                prevEl: ".par-l",
            },
            on: {
                init(sw) {
                    if (sw.params.slidesPerView >= sw.slides.length || sw.slides.length < 2) {
                        if (swiperPartnerGradient) {
                            swiperPartnerGradient.classList.add('off');
                        }
                    }
                },
                ...gradientUtils(swiperPartnerGradient)
            }
        });
    }
}
