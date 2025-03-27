interface CreateElementOptions {
    class?: string | string[];
    onClick?: (event: PointerEvent) => void;
    attributes?: Record<string, any>;
}

export const createElement = <
    K extends keyof HTMLElementTagNameMap,
    L extends keyof HTMLElementEventMap
>(
    tag: K,
    options: CreateElementOptions = {},
    listeners: Record<L, ((event: HTMLElementEventMap[L]) => void)> = {} as any,
    children: HTMLElement[] = []
): HTMLElementTagNameMap[K] => {
    const el = document.createElement(tag);

    if (Array.isArray(options.class)) {
        el.classList.add(...options.class);
    } else if (options.class) {
        el.classList.add(options.class);
    }

    for (const [key, val] of Object.entries(options.attributes || {})) {
        if (['for'].includes(key)) {
            el.setAttribute(key, val);
        } else {
            (el as any)[key] = val;
        }
    }

    for (const [event, handler] of Object.entries<(event: HTMLElementEventMap[L]) => void>(listeners)) {
        el.addEventListener(event, handler);
    }

    for (const child of children) {
        el.appendChild(child);
    }

    return el;
};

export const findParent = ($element: HTMLElement, check: ($el: HTMLElement) => boolean): HTMLElement | undefined => {
    while (($element = $element.parentElement) && !check($element)) {}
    return $element;
};

export const asImage = (content: string) => `<img src="${content}" alt=""\>`;
