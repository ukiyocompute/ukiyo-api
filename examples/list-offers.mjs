// List rentable GPUs and prices. Public endpoint: no API key needed. Node.js 18+, no dependencies.
const response = await fetch('https://pay.u-kiyo.ai/api/v1/offers');
const { data: offers } = await response.json();
for (const offer of offers.sort((a, b) => a.pricePerHourMinor - b.pricePerHourMinor).slice(0, 10)) {
  console.log(`${offer.name.padEnd(28)} x${offer.gpuCount}  $${(offer.pricePerHourMinor / 100).toFixed(2)}/hour  ${offer.id}`);
}
