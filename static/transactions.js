document.addEventListener("DOMContentLoaded", () => {
    const primarySelect = document.getElementById('primary-category');
    const subSelect = document.getElementById('sub-category');
    const typeSelect = document.getElementById('category-type');

    fetch('/categories')
        .then(response => response.json())
        .then(data => {
            for(const type in data) {
                const option = document.createElement('option');
                option.value = type;
                option.textContent = type;
                typeSelect.appendChild(option);
            }

            typeSelect.addEventListener('change', () => {
                const selectedType = typeSelect.value;
                primarySelect.innerHTML = '<option value="">Select Primary Category</option>';
                subSelect.innerHTML = '<option value="">Select Sub Category</option>';

                if(data[selectedType]){
                    for (const primary in data[selectedType]) {
                        const option = document.createElement('option');
                        option.value = primary;
                        option.textContent = primary;
                        primarySelect.appendChild(option);
                    }
                }
            });

            primarySelect.addEventListener('change', () => {
                const selectedType = typeSelect.value;
                const selectedPrimary = primarySelect.value;
                subSelect.innerHTML = '<option value="">Select Sub Category</option>';

                if (data[selectedType] && data[selectedType][selectedPrimary]) {
                    data[selectedType][selectedPrimary].forEach(sub => {
                        const option = document.createElement('option');
                        option.value = sub;
                        option.textContent = sub;
                        subSelect.appendChild(option);
                    });
                }
            });
        });
});







document.addEventListener('DOMContentLoaded', function() {
    const editButton = document.getElementById('btn-edit');

    editButton.addEventListener('click', async function() {
        const selectedTransaction = document.querySelector('input[name="edit-transact"]:checked');

        if (selectedTransaction) {
            const transactionId = selectedTransaction.value;
            try {
                const response = await fetch(`/edit_transaction/${transactionId}`);
                const data = await response.json();
                
                if (response.ok) {
                    
                    document.getElementById('edit-transaction-name').value = data.name;
                    document.getElementById('edit-transaction-date').value = data.date;
                    document.getElementById('edit-category-type').innerHTML = '<option value="" disabled selected>' + data.type +'</option>';
                    document.getElementById('edit-category-type').disabled = true;

                    document.getElementById('edit-primary-category').innerHTML = '<option value="" disabled selected>' + data.primary_category +'</option>';
                    document.getElementById('edit-primary-category').disabled = true;

                    document.getElementById('edit-sub-category').innerHTML = '<option value="" disabled selected>' + data.sub_category +'</option>';
                    document.getElementById('edit-sub-category').disabled = true;

                    document.getElementById('edit-transaction-amount').value = data.amount;
                    document.getElementById('edit-transfer-method').value = data.method;
                    document.getElementById('edit-description').value = data.description;
                    $('#edit-modal').modal('show');

                    
                    $('#edit-transaction-form').on('submit', function(event) {

                        event.preventDefault(); // Prevent default form submission
                        const transactionData = {
                            id: data.id, // The ID of the transaction being edited
                            name: $('#edit-transaction-name').val(),
                            date: $('#edit-transaction-date').val(),
                            amount: $('#edit-transaction-amount').val(),
                            type: $('#edit-transfer-method').val(),
                            description: $('#edit-description').val()
                            
                        };
                        
                        $.ajax({
                            url: '/edit_transaction/'+ data.id,
                            type: 'POST',
                            contentType: 'application/json',
                            data: JSON.stringify(transactionData), // Send data as JSON
                            
                            success: function(response) {
                                $('#edit-modal').modal('hide');
                                location.reload();

                            },
                            error: function(xhr) {
                                // Handle error
                                alert('Error: ' + xhr.responseJSON.error);
                            }
                        });
                    });
                    




                } else {
                    alert(data.error);  
                }
            } catch (error) {
                console.error('Error fetching transaction:', error);
            }






            
        } else {
            alert("Please select a transaction to edit.");
        }
    });





});



