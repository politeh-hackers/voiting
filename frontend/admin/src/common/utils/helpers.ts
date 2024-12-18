export function splitPrice(price) {
    const intPart = Math.floor(price);
    const floatPart = (price % 1).toFixed(2).substring(2);
    return {
        intPart: intPart.toString(),
        floatPart: floatPart
    };
}
