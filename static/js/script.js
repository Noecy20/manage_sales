fetch('/data')
.then(response => response.json())
.then(data => {
    // Extract monthly sales data
    const months = data.sales_data.map(item => item[0]);
    const sales = data.sales_data.map(item => item[1]);
    // Extract product sales data
    const products = data.product_sales.map(item => item[0]);
	// const types = data.product_sales.map(item => item[1]);
    const totalQuantity = data.product_sales.map(item => item[2]);
	const totalSales = data.product_sales.map(item => item[3]);
	// const users = data.product_sales.map(item => item[4]);
	// const u_name = data.product_sales.map(item => item[5]);

	const users = data.user_sales.map(item => item[0]);
    const utotalSales = data.user_sales.map(item => item[1]);


	const ttypes = data.type_sales.map(item => item[0]);
	const ttotalQuantity = data.type_sales.map(item => item[1]);
    const ttotalSales = data.type_sales.map(item => item[2]);
    
	// Extract overall average price
	const overallAvgPrice = data.overall_avg_price;

	// Extract product average prices
	const _products = data.product_avg_prices.map(item => item[0]);
	const avgPrices = data.product_avg_prices.map(item => item[1]);


    // Monthly Sales Chart
    const monthlySalesCtx = document.getElementById('monthlySalesChart').getContext('2d');
    new Chart(monthlySalesCtx, {
        type: 'bar',
        data: {
            labels: months,
            datasets: [{
                label: 'Ventes mensuelles',
                data: sales,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Product Sales Chart
    const productSalesCtx = document.getElementById('productSalesChart').getContext('2d');
    new Chart(productSalesCtx, {
        type: 'line',
        data: {
            labels: products,
            datasets: [
                {
                    label: 'Total des ventes',
                    data: totalSales,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                },
                {
                    label: 'Quantité vendue',
                    data: totalQuantity,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)',
                    borderColor: 'rgba(255, 99, 132, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });


	// User Sales Chart
	const userSalesCtx = document.getElementById('userSalesChart').getContext('2d');
	new Chart(userSalesCtx, {
		type: 'bar',
		data: {
			labels: users,
			datasets: [
				{
					label: 'Total des ventes',
					data: utotalSales,
					backgroundColor: 'rgba(75, 192, 192, 0.2)',
					borderColor: 'rgba(75, 192, 192, 1)',
					borderWidth: 1
				}
			]
		},
		options: {
			scales: {
				y: {
					beginAtZero: true
				}
			}
		}
	});

	// Type Sales Chart
	const _typeSalesCtx = document.getElementById('_typeSalesChart').getContext('2d');
	new Chart(_typeSalesCtx, {
		type: 'bar',
		data: {
			labels: ttypes,
			datasets: [
				{
					label: 'Total des ventes',
					data: ttotalSales,
					backgroundColor: 'rgba(75, 192, 192, 0.2)',
					borderColor: 'rgba(75, 192, 192, 1)',
					borderWidth: 1
				},
				{
					label: 'Quantité vendue',
					data: ttotalQuantity,
					backgroundColor: 'rgba(255, 99, 132, 0.2)',
					borderColor: 'rgba(255, 99, 132, 1)',
					borderWidth: 1
				}
			]
		},
		options: {
			scales: {
				y: {
					beginAtZero: true
				}
			}
		}
	});


    // Product Average Prices Chart
    const productAvgPricesCtx = document.getElementById('productAvgPricesChart').getContext('2d');
    new Chart(productAvgPricesCtx, {
        type: 'line',
        data: {
            labels: _products,
            datasets: [
                {
                    label: 'Prix moyen de vente',
                    data: avgPrices,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
                    borderWidth: 1
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Overall Average Price
    document.getElementById('overallAvgPrice').innerText = `Prix moyen de vente global: ${overallAvgPrice}`;
    // Best Selling Product
    document.getElementById('bestProduct').innerText = `Produit le plus vendu: ${data.best_product_id}`;
    // Top 5 Customers
    const topCustomers = data.top_clients.map(item => `<li>${item[0]}: ${item[1]}</li>`).join('');
    document.getElementById('topCustomers').innerHTML = topCustomers;
});