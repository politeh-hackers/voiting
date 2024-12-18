export const throttle = <A extends any[]>(fn: (...args: A) => void, timeout = 100) => {
    let _handle = null;

    return (...args: A) => {
        if (_handle != null) {
            clearTimeout(_handle);
        }
        _handle = setTimeout(() => fn(...args), timeout);
    };
};
