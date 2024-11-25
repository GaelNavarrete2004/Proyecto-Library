# translations.py
languages = {
    'es': {
        'change_language': 'Cambiar idioma',
        'book_rating': "Calificar libro",
        'rating_label': "Calificación (0.0 - 5.0):",
        'review_label': "Escribe una reseña:",
        'submit_button': "Calificar y Reseñar",
        'placeholder_text': "Escribe tu reseña aquí...",
        'success_message': "Calificación realizada con éxito.",
        'error_message': "No se pudo conectar a la base de datos.",
        'book': "Libro:",
        'review_error': "Error al calificar el libro:",
        'bd_error': "Error al actualizar la base de datos:",
        'pay_liquidated': "Saldo pendiente liquidado",
        'pay_confirmation': 'Has realizado el pago de tu saldo pendiente con éxito el día',
        'pay_confirm': 'Gracias por tu preferencia.',
        'pay': "Pagar",
        'pending_pay': "Saldo pendiente: $",
        'pending_pay2': "Saldo pendiente",
        'name_benef': "Nombre del beneficiario:",
        'card_number': "Número de tarjeta:",
        'card_month': "Mes de vencimiento:",
        'months': [
            "01 - Enero", "02 - Febrero", "03 - Marzo", "04 - Abril", "05 - Mayo", "06 - Junio",
            "07 - Julio", "08 - Agosto", "09 - Septiembre", "10 - Octubre", "11 - Noviembre", "12 - Diciembre"
        ],
        'expiration_year': "Año de vencimiento:",
        'error_name': "Por favor, ingrese el nombre del beneficiario.",
        'error_card': "Por favor, ingrese un número de tarjeta válido.",
        'luhn_erorr': "Número de tarjeta inválido según la verificación de Luhn.",
        'no_balance': "Actualmente no tienes saldo pendiente por pagar.",
        'valid_pay': "Pago exitoso",
        'payment_succes': "El pago se ha realizado con éxito.\nPuede que el pago tarde un poco en verse reflejado, reinicie la aplicación si el pago no se ve reflejado.",
        'email_confirmation': 'Correo enviado correctamente.',
        'email_error': 'Error al enviar el correo:',
        'not_valid_email': 'Correo no válido.',
        'register': 'Registrarse',
        'password': 'Contraseña:',
        'name': 'Nombre:',
        'last_name_father': 'Apellido Paterno:',
        'last_name_mother': 'Apellido Materno:',
        'email_error': 'Formato de correo inválido.',
        'password_error': 'La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula, un número y un carácter especial.',
        'name_error': 'El nombre es obligatorio y debe tener al menos 3 caracteres.',
        'last_name_father_error': 'El apellido paterno es obligatorio y debe tener al menos 3 caracteres.',
        'last_name_mother_error': 'El apellido materno es obligatorio y debe tener al menos 3 caracteres.',
        'register_confirmation': 'Registro exitoso',
        'register_user_id': 'ID del usuario registrado:',
        'register_error': 'Error al realizar el registro:',
        'buy': 'Comprar',
        'reserve': 'Reservar',
        'search_author': '   Buscar autor',
        'search_title': '   Buscar título',
        'search_genre': '   Buscar género',
        'search': 'Título, autor o género',
        'title': 'Título',
        'author': 'Autor',
        'genre': 'Género',
        'state': 'Estado',
        'calification': 'Calificación',
        'price': 'Precio',
        'search_tab': 'Buscar',
        'book_id': 'ID del libro',
        'book_title': 'Título del libro',
        'loan_date': 'Fecha de préstamo',
        'return_date': 'Fecha de devolución',
        'history': 'Historial de prestamos',
        'purchase_date': 'Fecha de compra',
        'purchase_history': 'Historial de compras',
        'cancel_reserve': 'Cancelar reserva',
        'return_book': 'Devolver libro',
        'book_calification': 'Calificar libro',
        'my_califications': 'Mis calificación',
        'my_books': 'Mis libros',
        'login': 'Iniciar sesión',
        'register_text': '¿No tienes cuenta? Regístrate',
        'mail': 'Correo electrónico:',
        'signup': 'Registrarse',
        'enter': 'Ingresar',
        'account': 'Cuenta',    
        'logout': '  Cerrar Sesión',
        'pay_balance': '   Pagar Saldo',
        'user_info': 'Datos de usuario',
        'search_book_id': 'ID del libro a buscar',
        'review': 'Reseña',
        'calification_plural': 'Calificaciones',
        'inserted_user_id': 'ID del usuario insertado: ',
        'insert_emailandpassword': 'Por favor, ingrese su correo electrónico y contraseña.',
        'name_4': 'Nombre: ',
        'login_confirmation': 'Inicio de sesión exitoso',
        'welcome': 'Bienvenido',
        'wrong_credentials': 'Credenciales inválidas.\n¿El usuario está registrado?',
        'login_erorr': 'Error al iniciar sesión: ',
        'warning': 'Advertencia',
        'id_not_found': 'No se pudo obtener el ID del usuario.',
        'not_credentials': 'El archivo de credenciales no tiene un formato JSON válido o la clave de encriptación es incorrecta.',
        'user_not_found': 'Usuario no encontrado.',
        'user_not_match': 'No se encontró un usuario con este correo.',
        'error_obtain_id': 'Error al obtener el ID del usuario.',
        'sanction_applied': 'Sanción aplicada',
        'sanction_info': 'Se ha aplicado una multa de',
        'sanction_info2': 'unidades por',
        'sanction_info3': 'días de retraso.',
        'sanction_info4': 'Se ha cancelado la cuenta del usuario por más de 7 días de retraso.',
        'information': 'Información',
        'no_books_returned': 'No hay libros devueltos a tiempo.',
        'account': 'Cuenta',
        'error_search': 'Primero escribe algo en el buscador.',
        'no_results': 'No se encontraron resultados para el',
        'error_results': 'Error al mostrar los resultados.',
        'available': 'Disponible',
        'not_available': 'No disponible',
        'response_error': 'Error al ejecturar consulta:',
        'reserved_log': 'Debes iniciar sesión para reservar un libro.',
        'reserved_info': 'El costo por reserva de cada libro es de $7.00 MXN por día, se te dará un limite de 15 días para retornarlo. Si no se devuelve a tiempo se cobrará una multa de $20 por cáda día que pase.\n(Es posible devolver antes el libro, solo se te cobrará lo correspondiente)',
        'book_not_available': 'El libro seleccionado no está disponible.',
        'book_select': 'Selecciona un libro para reservar.',
        'book_buy_log': 'Debes iniciar sesión para comprar un libro.',
        'book_buy_select': 'Selecciona un libro para comprar.',
        'book_buy_not_available': 'No hay libros disponibles para comprar',
        'comprar_libro': 'Comprar libro',
        'confirm_buy': 'Confirmar compra del libro: ',
        'book_success': 'Libro comprado con éxito.',
        'book_reserve_success': 'Libro reservado con éxito.',
        'insert_data_correct': 'Datos insertados correctamente.',
        'insert_data_error': 'Error al insertar datos.',
        'mybooks_log': 'Debes iniciar sesión para ver tus libros.',
        'reserved': 'Reservado',
        'buyed': 'Comprado',
        'returned': 'Devuelto',
        'canceled': 'Cancelado',
        'no_books': 'No tienes libros reservados',
        'history_log': 'Debes iniciar sesión para ver tu historial.',
        'no_books_history': 'No tienes historial de prestamos.',
        'reserve_cancel': 'Cancelación de reserva',
        'reserved_cancel': 'Reserva cancelada con éxito.',
        'reserved_cancel_error': 'Error al cancelar la reserva: ',
        'reserved_cancel_day': 'Solo puedes cancelar reservas que se han hecho el mismo día.',
        'congratulations': '¡Felicidades!',
        'discount_obtain': 'Has obtenido un descuento por devolver el libro antes de tiempo.',
        'returned_reserve': 'Devolución de reserva',
        'book_returned': 'Libro devuelto con éxito. \nCosto: $',
        'book_returned_error': 'Error al devolver reserva: ',
        'saldo_pending': 'Saldo pendiente: $',
        'not_saldo_pending': 'Actualmente no tienes saldo pendiente por pagar.',
        'select_book': 'Selecciona un libro para calificar.',
        'send_email': 'Enviar correo',

    },
    'en': {
        'change_language': 'Change language',
        'book_rating': "Rate Book",
        'rating_label': "Rating (0.0 - 5.0):",
        'review_label': "Write a review:",
        'submit_button': "Rate and Review",
        'placeholder_text': "Write your review here...",
        'success_message': "Rating submitted successfully.",
        'error_message': "Could not connect to the database.",
        'book': "Book:",
        'review_error': "Error rating the book:",
        'bd_error': "Error updating the database:",
        'pay_liquidated': "Pending balance liquidated",
        'pay_confirmation': 'You have successfully paid your pending balance on',
        'pay_confirm': 'Thank you for your preference.',
        'pay': "Pay",
        'pending_pay': "Pending balance: $",
        'pending_pay2': "Pending balance",
        'name_benef': "Beneficiary's name:",
        'card_number': "Card number:",
        'card_month': "Expiration month:",
        'months': [
            "01 - January", "02 - February", "03 - March", "04 - April", "05 - May", "06 - June",
            "07 - July", "08 - August", "09 - September", "10 - October", "11 - November", "12 - December"
        ],
        'expiration_year': "Expiration year:",
        'error_name': "Please enter the beneficiary's name.",
        'error_card': "Please enter a valid card number.",
        'luhn_erorr': "Invalid card number according to Luhn verification.",
        'no_balance': "You currently have no pending balance to pay.",
        'valid_pay': "Successful payment",
        'payment_succes': "The payment has been made successfully.\nIt may take a while for the payment to be reflected, restart the application if the payment is not reflected.",
        'email_confirmation': 'Email sent successfully.',
        'email_error': 'Error sending email:',
        'not_valid_email': 'Invalid email.',
        'register': 'Register',
        'password': 'Password:',
        'name': 'Name:',
        'last_name_father': 'Father\'s Last Name:',
        'last_name_mother': 'Mother\'s Last Name:',
        'email_error': 'Invalid email format.',
        'password_error': 'The password must be at least 8 characters, one uppercase, one lowercase, one number and one special character.',
        'name_error': 'The name is required and must be at least 3 characters.',
        'last_name_father_error': 'The father\'s last name is required and must be at least 3 characters.',
        'last_name_mother_error': 'The mother\'s last name is required and must be at least 3 characters.',
        'register_confirmation': 'Successful registration',
        'register_user_id': 'Registered user ID:',
        'register_error': 'Error registering user:',
        'buy': 'Buy',
        'reserve': 'Reserve',
        'search_author': '   Search author',
        'search_title': '   Search title',
        'search_genre': '   Search genre',
        'search': 'Title, author or genre',
        'title': 'Title',
        'author': 'Author',
        'genre': 'Genre',
        'state': 'State',
        'calification': 'Calification',
        'price': 'Price',
        'search_tab': 'Search',
        'book_id': 'Book ID',
        'book_title': 'Book Title',
        'loan_date': 'Loan Date',
        'return_date': 'Return Date',
        'history': 'Loan history',
        'purchase_date': 'Purchase Date',
        'purchase_history': 'Purchase history',
        'cancel_reserve': 'Cancel reserve',
        'return_book': 'Return book',
        'book_calification': 'Rate book',
        'my_califications': 'My calification',
        'my_books': 'My books',
        'login': 'Log in',
        'register_text': 'Don\'t have an account? Register',
        'mail': 'Email:',
        'signup': 'Sign up',
        'enter': 'Enter',
        'account': 'Account',
        'logout': '  Log out',
        'pay_balance': '   Pay Balance',
        'user_info': 'User information',
        'search_book_id': 'Book ID to search',
        'review': 'Review',
        'calification_plural': 'Califications',
        'inserted_user_id': 'Inserted user ID: ',
        'insert_emailandpassword': 'Please enter your email and password.',
        'name_4': 'Name: ',
        'login_confirmation': 'Successful login',
        'welcome': 'Welcome',
        'wrong_credentials': 'Invalid credentials.\nIs the user registered?',
        'login_erorr': 'Error logging in: ',
        'warning': 'Warning',
        'id_not_found': 'Could not get the user ID.',
        'not_credentials': 'The credentials file does not have a valid JSON format or the encryption key is incorrect.',
        'user_not_found': 'User not found.',
        'user_not_match': 'No user found with this email.',
        'error_obtain_id': 'Error obtaining the user ID.',
        'sanction_applied': 'Sanction applied',
        'sanction_info': 'A fine of',
        'sanction_info2': 'units has been applied for',
        'sanction_info3': 'days of delay.',
        'sanction_info4': 'The user account has been canceled for more than 7 days of delay.',
        'information': 'Information',
        'no_books_returned': 'No books returned on time.', 
        'account': 'Account',
        'error_search': 'First write something in the search bar.',
        'no_results': 'No results found for',
        'error_results': 'Error showing results.',
        'available': 'Disponible',
        'not_available': 'No disponible',
        'response_error': 'Error executing query:',
        'reserved_log': 'You must log in to reserve a book.',
        'reserved_info': 'The cost per reservation of each book is $7.00 MXN per day, you will be given a limit of 15 days to return it. If it is not returned on time, a fine of $20 will be charged for each day that passes.\n(It is possible to return the book earlier, you will only be charged the corresponding amount)',
        'book_not_available': 'The selected book is not available.',
        'book_select': 'Select a book to reserve.',
        'book_buy_log': 'You must log in to buy a book.',
        'book_buy_select': 'Select a book to buy.',
        'book_buy_not_available': 'There are no books available to buy',
        'comprar_libro': 'Buy book',
        'confirm_buy': 'Confirm purchase of the book: ',
        'book_success': 'Book purchased successfully.',
        'insert_data_correct': 'Data inserted correctly.',
        'insert_data_error': 'Error inserting data.',
        'mybooks_log': 'You must log in to see your books.',
        'reserved': 'Reserved',
        'buyed': 'Bought',
        'returned': 'Returned',
        'canceled': 'Canceled',
        'no_books': 'You have no reserved books',
        'history_log': 'You must log in to see your history.',
        'no_books_history': 'You have no loan history.',
        'reserved_cancel': 'Reservation canceled successfully.',
        'reserve_cancel': 'Reservation cancellation',
        'reserved_cancel_error': 'Error canceling reservation: ',
        'reserved_cancel_day': 'You can only cancel reservations made on the same day.',
        'congratulations': 'Congratulations!',
        'discount_obtain': 'You have obtained a discount for returning the book early.',
        'returned_reserve': 'Return reservation',
        'book_returned': 'Book returned successfully. \nCost: $',
        'book_returned_error': 'Error returning reservation: ',
        'saldo_pending': 'Pending balance: $',
        'not_saldo_pending': 'You currently have no pending balance to pay.',
        'select_book': 'Select a book to rate.',
        'book_reserve_success': 'Book reserved successfully.',
        'send_email': 'Send email',
    }
}