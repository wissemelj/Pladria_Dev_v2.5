
// Pladria Statistics Updated: 2025-07-24 14:00:15
// Period: 2025-05-01 to 2025-07-24
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 23:59:05
// Period: 2025-07-02 to 2025-07-23
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 23:30:46
// Period: 2025-07-01 to 2025-07-16
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 15:26:52
// Period: 2025-05-01 to 2025-07-23
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 15:08:49
// Period: 2025-05-01 to 2025-07-23
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 15:01:14
// Period: 2025-05-01 to 2025-07-23
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 14:38:04
// Period: 2025-05-01 to 2025-07-23
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 14:28:57
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 14:13:56
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 14:09:34
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 14:01:31
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 13:30:59
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 13:18:43
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 13:11:16
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 12:56:49
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 12:46:42
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 12:44:45
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 12:40:46
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 12:29:38
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 12:22:42
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 12:09:52
// Period: 2025-07-01 to 2025-07-10
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 11:56:27
// Period: 2025-07-01 to 2025-07-11
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 11:55:48
// Period: 2025-07-01 to 2025-07-15
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 11:55:38
// Period: 2025-07-01 to 2025-07-16
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 11:55:29
// Period: 2025-07-01 to 2025-07-16
// Total Records: 0

// Pladria Statistics Updated: 2025-07-23 11:55:15
// Period: 2025-07-01 to 2025-07-16
// Total Records: 0
// Configuration globale pour Chart.js
Chart.defaults.responsive = true;
Chart.defaults.maintainAspectRatio = false;
Chart.defaults.plugins.legend.position = 'bottom';

// Couleurs personnalisées
const colors = {
    orange: '#ff6b35',
    rip: '#e74c3c',
    raf: '#3498db',
    modif: '#f39c12',
    crea: '#27ae60',
    adNonJointe: '#9b59b6',
    adNonTrouvee: '#e67e22',
    horsCommune: '#34495e',
    nok: '#e74c3c',
    ok: '#27ae60',
    avecTemps: '#2ecc71',
    sansTemps: '#95a5a6',
    uprNok: '#e74c3c',
    uprOk: '#27ae60',
    uprRas: '#3498db',
    uprCree: '#27ae60',
    uprNon: '#e74c3c',
    tickets501511: '#9b59b6',
    ripRien: '#3498db',
    ripModification: '#f39c12',
    ripCreation: '#27ae60',
    verified: '#27ae60',
    errorRate: '#e67e22'
};

// Graphique Communes livrées
const communesCtx = document.getElementById('communesChart').getContext('2d');
new Chart(communesCtx, {
    type: 'doughnut',
    data: {
        labels: ['Orange', 'RIP'],
        datasets: [{
            data: [87, 12],
            backgroundColor: [colors.orange, colors.rip],
            borderWidth: 2,
            borderColor: '#fff'
        }]
    },
    options: {
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true
                }
            }
        }
    }
});

// Graphique CM
const cmCtx = document.getElementById('cmChart').getContext('2d');
new Chart(cmCtx, {
    type: 'bar',
    data: {
        labels: ['RAF', 'MODIF', 'CREA'],
        datasets: [{
            data: [1573, 24, 124],
            backgroundColor: [colors.raf, colors.modif, colors.crea],
            borderColor: [colors.raf, colors.modif, colors.crea],
            borderWidth: 2,
            borderRadius: 5,
            borderSkipped: false
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0,0,0,0.1)',
                    lineWidth: 1
                },
                ticks: {
                    font: {
                        size: 12,
                        weight: 'bold'
                    },
                    color: '#2c3e50'
                },
                title: {
                    display: true,
                    text: 'Nombre',
                    font: {
                        size: 12,
                        weight: 'bold'
                    },
                    color: '#2c3e50'
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    font: {
                        size: 11,
                        weight: 'bold'
                    },
                    color: '#2c3e50'
                }
            }
        }
    }
});

// Graphique Contrôle Qualité
const qualityCtx = document.getElementById('qualityChart').getContext('2d');
new Chart(qualityCtx, {
    type: 'doughnut',
    data: {
        labels: ['conformes', 'non conformes'],
        datasets: [{
            data: [37, 25], 
            backgroundColor: [colors.verified, colors.errorRate],
            borderWidth: 2,
            borderColor: '#fff'
        }]
    },
    options: {
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true,
                    generateLabels: function(chart) {
                        return [
                            {
                                text: 'conformes',
                                fillStyle: colors.verified,
                                strokeStyle: colors.verified,
                                pointStyle: 'circle'
                            },
                            {
                                text: 'non conformes',
                                fillStyle: colors.errorRate,
                                strokeStyle: colors.errorRate,
                                pointStyle: 'circle'
                            }
                        ];
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        if (context.dataIndex === 0) {
                            return 'conformes: 60% - 37 communes';
                        } else {
                            return 'non conformes: 40%  - 25 communes';
                        }
                    }
                }
            }
        }
    }
});

// Graphique Acts traitement PA (principal)
const actsCtx = document.getElementById('actsChart').getContext('2d');
new Chart(actsCtx, {
    type: 'bar',
    data: {
        labels: ['AD RAS\nsans temps', 'AD RAS\navec temps', 'OK', 'NOK', 'AD Non jointe', 'UPR RAS', 'AD Non trouvée', 'Hors commune', 'UPR NOK', 'UPR OK'],
        datasets: [{
            data: [13247, 4862, 2388, 1740, 893, 498, 285, 39, 45, 34],
            backgroundColor: [
                colors.avecTemps,
                colors.sansTemps,
                colors.adNonJointe,
                colors.adNonTrouvee,
                colors.horsCommune,
                colors.nok,
                colors.ok,
                colors.uprRas,
                colors.uprNok,
                colors.uprOk
            ],
            borderColor: [
                colors.avecTemps,
                colors.sansTemps,
                colors.adNonJointe,
                colors.adNonTrouvee,
                colors.horsCommune,
                colors.nok,
                colors.ok,
                colors.uprRas,
                colors.uprNok,
                colors.uprOk
            ],
            borderWidth: 2,
            borderRadius: 8,
            borderSkipped: false
        }]
    },
    options: {
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        const percentage = ((context.raw / total) * 100).toFixed(1);
                        return `${context.label.replace('\n', ' ')}: ${context.raw.toLocaleString()} (${percentage}%)`;
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0,0,0,0.1)',
                    lineWidth: 1
                },
                ticks: {
                    callback: function(value) {
                        return value.toLocaleString();
                    },
                    font: {
                        size: 12,
                        weight: 'bold'
                    },
                    color: '#2c3e50'
                },
                title: {
                    display: true,
                    text: 'Nombre d\'actes',
                    font: {
                        size: 14,
                        weight: 'bold'
                    },
                    color: '#2c3e50'
                }
            },
            x: {
                grid: {
                    display: false
                },
                ticks: {
                    maxRotation: 45,
                    font: {
                        size: 11,
                        weight: 'bold'
                    },
                    color: '#2c3e50'
                },
                title: {
                    display: true,
                    text: 'Catégories',
                    font: {
                        size: 14,
                        weight: 'bold'
                    },
                    color: '#2c3e50'
                }
            }
        }
    }
});

// Note: UPR and 501/511 sections use simple number displays instead of charts

// Graphique RIP (P0 P1)
const ripCtx = document.getElementById('ripChart').getContext('2d');
new Chart(ripCtx, {
    type: 'doughnut',
    data: {
        labels: ['Rien à faire', 'Modification', 'Création'],
        datasets: [{
            data: [0, 0, 0],
            backgroundColor: [
                colors.ripRien,
                colors.ripModification,
                colors.ripCreation
            ],
            borderColor: [
                colors.ripRien,
                colors.ripModification,
                colors.ripCreation
            ],
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                position: 'bottom',
                labels: {
                    padding: 20,
                    usePointStyle: true,
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        const total = context.dataset.data.reduce((a, b) => a + b, 0);
                        if (total === 0) {
                            return context.label + ': 0 (0%)';
                        }
                        const percentage = ((context.parsed / total) * 100).toFixed(1);
                        return context.label + ': ' + context.parsed + ' (' + percentage + '%)';
                    }
                }
            }
        }
    }
});



// Facturation (Billing) System - Individual Motif Pricing
class DetailedBillingCalculator {
    constructor() {
        // PA (Acts) motifs data - order matches the Acts chart order
        this.paMotifs = [
            { id: 'ad-ras-sans', label: 'AD RAS sans temps', defaultCount: 13244 },
            { id: 'ad-ras-avec', label: 'AD RAS avec temps', defaultCount: 4889 },
            { id: 'ok', label: 'OK', defaultCount: 2391 },
            { id: 'nok', label: 'NOK', defaultCount: 1775 },
            { id: 'ad-non-jointe', label: 'AD Non jointe', defaultCount: 893 },
            { id: 'upr-ras', label: 'UPR RAS', defaultCount: 499 },
            { id: 'ad-non-trouvee', label: 'AD Non trouvée', defaultCount: 285 },
            { id: 'hors-commune', label: 'Hors commune', defaultCount: 39 },
            { id: 'upr-nok', label: 'UPR NOK', defaultCount: 45 },
            { id: 'upr-ok', label: 'UPR OK', defaultCount: 34 }
        ];

        // CM motifs data - order matches the CM chart order
        this.cmMotifs = [
            { id: 'raf', label: 'RAF', defaultCount: 1573 },
            { id: 'modification', label: 'Modification', defaultCount: 24 },
            { id: 'creation', label: 'Création', defaultCount: 124 }
        ];

        // UPR motifs data - order matches the UPR data order
        this.uprMotifs = [
            { id: 'upr-cree', label: 'UPR Créé', defaultCount: 16 },
            { id: 'upr-non', label: 'UPR Non', defaultCount: 83 }
        ];

        // 501/511 tickets data
        this.tickets501511Motifs = [
            { id: 'tickets-501511', label: 'Tickets 501/511', defaultCount: 98 }
        ];

        this.init();
    }

    init() {
        // Initialize counts with default data
        this.updateCounts();

        // Add event listeners for all price inputs
        this.addEventListeners();

        // Initial calculation
        this.calculateAllPrices();
    }

    addEventListeners() {
        // PA motif price inputs
        this.paMotifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            if (priceInput) {
                priceInput.addEventListener('input', () => this.calculateAllPrices());
            }
        });

        // CM motif price inputs
        this.cmMotifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            if (priceInput) {
                priceInput.addEventListener('input', () => this.calculateAllPrices());
            }
        });

        // UPR motif price inputs
        this.uprMotifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            if (priceInput) {
                priceInput.addEventListener('input', () => this.calculateAllPrices());
            }
        });

        // 501/511 tickets price inputs
        this.tickets501511Motifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            if (priceInput) {
                priceInput.addEventListener('input', () => this.calculateAllPrices());
            }
        });
    }

    updateCounts() {
        // Update PA counts
        this.paMotifs.forEach((motif, index) => {
            const countElement = document.getElementById(`count-${motif.id}`);
            if (countElement) {
                countElement.textContent = motif.defaultCount.toLocaleString();
            }
        });

        // Update CM counts
        this.cmMotifs.forEach((motif, index) => {
            const countElement = document.getElementById(`count-${motif.id}`);
            if (countElement) {
                countElement.textContent = motif.defaultCount.toLocaleString();
            }
        });

        // Update UPR counts
        this.uprMotifs.forEach((motif, index) => {
            const countElement = document.getElementById(`count-${motif.id}`);
            if (countElement) {
                countElement.textContent = motif.defaultCount.toLocaleString();
            }
        });

        // Update 501/511 counts
        this.tickets501511Motifs.forEach((motif, index) => {
            const countElement = document.getElementById(`count-${motif.id}`);
            if (countElement) {
                countElement.textContent = motif.defaultCount.toLocaleString();
            }
        });
    }

    calculateAllPrices() {
        let totalPA = 0;
        let totalCM = 0;
        let totalUPR = 0;
        let total501511 = 0;

        // Calculate PA totals
        this.paMotifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            const totalElement = document.getElementById(`total-${motif.id}`);

            if (priceInput && totalElement) {
                const price = parseFloat(priceInput.value) || 0;
                const count = motif.defaultCount;
                const total = count * price;

                totalElement.textContent = this.formatCurrency(total);
                totalPA += total;
            }
        });

        // Calculate CM totals
        this.cmMotifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            const totalElement = document.getElementById(`total-${motif.id}`);

            if (priceInput && totalElement) {
                const price = parseFloat(priceInput.value) || 0;
                const count = motif.defaultCount;
                const total = count * price;

                totalElement.textContent = this.formatCurrency(total);
                totalCM += total;
            }
        });

        // Calculate UPR totals
        this.uprMotifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            const totalElement = document.getElementById(`total-${motif.id}`);

            if (priceInput && totalElement) {
                const price = parseFloat(priceInput.value) || 0;
                const count = motif.defaultCount;
                const total = count * price;

                totalElement.textContent = this.formatCurrency(total);
                totalUPR += total;
            }
        });

        // Calculate 501/511 totals
        this.tickets501511Motifs.forEach(motif => {
            const priceInput = document.getElementById(`price-${motif.id}`);
            const totalElement = document.getElementById(`total-${motif.id}`);

            if (priceInput && totalElement) {
                const price = parseFloat(priceInput.value) || 0;
                const count = motif.defaultCount;
                const total = count * price;

                totalElement.textContent = this.formatCurrency(total);
                total501511 += total;
            }
        });

        // Update section totals
        const totalPAElement = document.getElementById('totalPA');
        const totalCMElement = document.getElementById('totalCM');
        const totalUPRElement = document.getElementById('totalUPR');
        const total501511Element = document.getElementById('total501511');
        const grandTotalElement = document.getElementById('grandTotal');

        if (totalPAElement) {
            totalPAElement.textContent = this.formatCurrency(totalPA);
        }
        if (totalCMElement) {
            totalCMElement.textContent = this.formatCurrency(totalCM);
        }
        if (totalUPRElement) {
            totalUPRElement.textContent = this.formatCurrency(totalUPR);
        }
        if (total501511Element) {
            total501511Element.textContent = this.formatCurrency(total501511);
        }
        if (grandTotalElement) {
            grandTotalElement.textContent = this.formatCurrency(totalPA + totalCM + totalUPR + total501511);
        }
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'EUR',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        }).format(amount);
    }

    // Method to update with real data from Python
    updateWithRealData(paData, cmData, uprData, tickets501511Data) {
        // Update PA data
        if (paData && Array.isArray(paData)) {
            this.paMotifs.forEach((motif, index) => {
                if (index < paData.length) {
                    motif.defaultCount = paData[index];
                    const countElement = document.getElementById(`count-${motif.id}`);
                    if (countElement) {
                        countElement.textContent = paData[index].toLocaleString();
                    }
                }
            });
        }

        // Update CM data
        if (cmData && Array.isArray(cmData)) {
            this.cmMotifs.forEach((motif, index) => {
                if (index < cmData.length) {
                    motif.defaultCount = cmData[index];
                    const countElement = document.getElementById(`count-${motif.id}`);
                    if (countElement) {
                        countElement.textContent = cmData[index].toLocaleString();
                    }
                }
            });
        }

        // Update UPR data
        if (uprData && Array.isArray(uprData)) {
            this.uprMotifs.forEach((motif, index) => {
                if (index < uprData.length) {
                    motif.defaultCount = uprData[index];
                    const countElement = document.getElementById(`count-${motif.id}`);
                    if (countElement) {
                        countElement.textContent = uprData[index].toLocaleString();
                    }
                }
            });
        }

        // Update 501/511 data
        if (tickets501511Data && Array.isArray(tickets501511Data)) {
            this.tickets501511Motifs.forEach((motif, index) => {
                if (index < tickets501511Data.length) {
                    motif.defaultCount = tickets501511Data[index];
                    const countElement = document.getElementById(`count-${motif.id}`);
                    if (countElement) {
                        countElement.textContent = tickets501511Data[index].toLocaleString();
                    }
                }
            });
        }

        // Recalculate with new data
        this.calculateAllPrices();
    }
}

// Initialize detailed billing calculator when DOM is loaded
let detailedBillingCalculator;

// Animation d'entrée pour les cartes
document.addEventListener('DOMContentLoaded', function() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
    });

    // Initialize detailed billing calculator
    detailedBillingCalculator = new DetailedBillingCalculator();
});

// Update detailed facturation data with real values
if (typeof detailedBillingCalculator !== 'undefined' && detailedBillingCalculator) {
    detailedBillingCalculator.updateWithRealData([6029, 2374, 1082, 942, 584, 207, 143, 23, 17, 16], [806, 17, 71], [11, 49], [45]);
}

// Update detailed facturation data with real values
if (typeof detailedBillingCalculator !== 'undefined' && detailedBillingCalculator) {
    detailedBillingCalculator.updateWithRealData([7987, 2971, 1297, 1144, 619, 240, 175, 23, 18, 16], [956, 10, 60], [11, 59], [55]);
}

// Update detailed facturation data with real values
if (typeof detailedBillingCalculator !== 'undefined' && detailedBillingCalculator) {
    detailedBillingCalculator.updateWithRealData([13247, 4862, 2388, 1740, 893, 498, 285, 39, 45, 34], [1573, 24, 124], [16, 83], [98]);
}
