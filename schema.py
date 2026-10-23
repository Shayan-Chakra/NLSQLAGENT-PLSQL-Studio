"""Database schema metadata for NLSQLAGENT.

Both the Gemini prompt and SQL validator can read this structure so they use
consistent table and column names. These definitions describe the intended
schema; they do not create the tables in Oracle. Create the corresponding
Oracle tables and grant access before querying newly added domains.
"""

SCHEMA = {
    # Existing HR tables
    "EMPLOYEES": {
        "description": "one row per employee",
        "columns": {
            "EMPLOYEE_ID": "primary key; employee number",
            "EMPLOYEE_NAME": "employee name",
            "SALARY": "employee salary",
            "DEPARTMENT_ID": "department number; references DEPARTMENTS.DEPARTMENT_ID",
        },
    },
    "DEPARTMENTS": {
        "description": "one row per department",
        "columns": {
            "DEPARTMENT_ID": "primary key; department number",
            "DEPARTMENT_NAME": "department name",
            "LOCATION": "city where the department is based",
        },
    },

    # Education domain
    "SCHOOLS": {
        "description": "one row per school or educational institution",
        "columns": {
            "SCHOOL_ID": "primary key; school identifier",
            "SCHOOL_NAME": "name of the school or institution",
            "SCHOOL_TYPE": "school type, such as primary, secondary, college, or university",
            "CITY": "city where the school is located",
        },
    },
    "STUDENTS": {
        "description": "one row per student",
        "columns": {
            "STUDENT_ID": "primary key; student identifier",
            "FIRST_NAME": "student first name",
            "LAST_NAME": "student last name",
            "DATE_OF_BIRTH": "student date of birth",
            "EMAIL": "student email address",
            "SCHOOL_ID": "school identifier; references SCHOOLS.SCHOOL_ID",
        },
    },
    "TEACHERS": {
        "description": "one row per teacher or instructor",
        "columns": {
            "TEACHER_ID": "primary key; teacher identifier",
            "TEACHER_NAME": "teacher full name",
            "EMAIL": "teacher email address",
            "SUBJECT_AREA": "subject or discipline taught",
            "SCHOOL_ID": "school identifier; references SCHOOLS.SCHOOL_ID",
        },
    },
    "COURSES": {
        "description": "one row per course offered by a school",
        "columns": {
            "COURSE_ID": "primary key; course identifier",
            "COURSE_NAME": "course title",
            "CREDITS": "number of course credits",
            "TEACHER_ID": "instructor identifier; references TEACHERS.TEACHER_ID",
            "SCHOOL_ID": "school identifier; references SCHOOLS.SCHOOL_ID",
        },
    },
    "ENROLLMENTS": {
        "description": "one row per student's enrollment in a course",
        "columns": {
            "ENROLLMENT_ID": "primary key; enrollment identifier",
            "STUDENT_ID": "student identifier; references STUDENTS.STUDENT_ID",
            "COURSE_ID": "course identifier; references COURSES.COURSE_ID",
            "ENROLLMENT_DATE": "date the student enrolled",
            "GRADE": "grade or result awarded for the course",
        },
    },

    # Healthcare domain
    "HOSPITALS": {
        "description": "one row per hospital or healthcare facility",
        "columns": {
            "HOSPITAL_ID": "primary key; hospital identifier",
            "HOSPITAL_NAME": "hospital or facility name",
            "LOCATION": "hospital address or city",
            "PHONE": "hospital contact number",
        },
    },
    "DOCTORS": {
        "description": "one row per doctor or clinician",
        "columns": {
            "DOCTOR_ID": "primary key; doctor identifier",
            "DOCTOR_NAME": "doctor full name",
            "SPECIALIZATION": "medical specialization",
            "PHONE": "doctor contact number",
            "HOSPITAL_ID": "hospital identifier; references HOSPITALS.HOSPITAL_ID",
        },
    },
    "PATIENTS": {
        "description": "one row per patient",
        "columns": {
            "PATIENT_ID": "primary key; patient identifier",
            "PATIENT_NAME": "patient full name",
            "DATE_OF_BIRTH": "patient date of birth",
            "PHONE": "patient contact number",
            "BLOOD_GROUP": "patient blood group, if recorded",
        },
    },
    "APPOINTMENTS": {
        "description": "one row per patient appointment",
        "columns": {
            "APPOINTMENT_ID": "primary key; appointment identifier",
            "PATIENT_ID": "patient identifier; references PATIENTS.PATIENT_ID",
            "DOCTOR_ID": "doctor identifier; references DOCTORS.DOCTOR_ID",
            "HOSPITAL_ID": "hospital identifier; references HOSPITALS.HOSPITAL_ID",
            "APPOINTMENT_DATE": "date and time of appointment",
            "STATUS": "appointment status, such as scheduled, completed, or cancelled",
        },
    },
    "MEDICAL_RECORDS": {
        "description": "one row per patient clinical record or visit summary",
        "columns": {
            "RECORD_ID": "primary key; medical record identifier",
            "PATIENT_ID": "patient identifier; references PATIENTS.PATIENT_ID",
            "DOCTOR_ID": "doctor identifier; references DOCTORS.DOCTOR_ID",
            "RECORD_DATE": "date of the clinical record",
            "DIAGNOSIS": "diagnosis or assessment",
            "NOTES": "clinical notes; sensitive health information",
        },
    },
    "PRESCRIPTIONS": {
        "description": "one row per medication prescribed to a patient",
        "columns": {
            "PRESCRIPTION_ID": "primary key; prescription identifier",
            "PATIENT_ID": "patient identifier; references PATIENTS.PATIENT_ID",
            "DOCTOR_ID": "prescribing doctor; references DOCTORS.DOCTOR_ID",
            "MEDICATION_NAME": "prescribed medication name",
            "DOSAGE": "prescribed dosage instructions",
            "PRESCRIBED_DATE": "date the medication was prescribed",
        },
    },

    # Sales and retail domain
    "CUSTOMERS": {
        "description": "one row per customer",
        "columns": {
            "CUSTOMER_ID": "primary key; customer identifier",
            "CUSTOMER_NAME": "customer full name or business name",
            "EMAIL": "customer email address",
            "PHONE": "customer contact number",
            "CITY": "customer city",
        },
    },
    "PRODUCTS": {
        "description": "one row per product offered for sale",
        "columns": {
            "PRODUCT_ID": "primary key; product identifier",
            "PRODUCT_NAME": "product name",
            "CATEGORY": "product category",
            "UNIT_PRICE": "price per unit",
            "STOCK_QUANTITY": "quantity currently in stock",
        },
    },
    "SALES_ORDERS": {
        "description": "one row per customer order",
        "columns": {
            "ORDER_ID": "primary key; sales order identifier",
            "CUSTOMER_ID": "customer identifier; references CUSTOMERS.CUSTOMER_ID",
            "ORDER_DATE": "date the order was placed",
            "ORDER_STATUS": "order status, such as pending, shipped, or cancelled",
        },
    },
    "SALES_ORDER_ITEMS": {
        "description": "one row per product line in a sales order",
        "columns": {
            "ORDER_ITEM_ID": "primary key; order line identifier",
            "ORDER_ID": "order identifier; references SALES_ORDERS.ORDER_ID",
            "PRODUCT_ID": "product identifier; references PRODUCTS.PRODUCT_ID",
            "QUANTITY": "number of product units ordered",
            "UNIT_PRICE": "unit price charged on this order line",
        },
    },
    "PAYMENTS": {
        "description": "one row per payment associated with an order",
        "columns": {
            "PAYMENT_ID": "primary key; payment identifier",
            "ORDER_ID": "order identifier; references SALES_ORDERS.ORDER_ID",
            "PAYMENT_DATE": "date the payment was made",
            "AMOUNT": "payment amount",
            "PAYMENT_METHOD": "payment method, such as card or bank transfer",
            "PAYMENT_STATUS": "payment status",
        },
    },

    # Library domain
    "BOOKS": {
        "description": "one row per library book or catalog item",
        "columns": {
            "BOOK_ID": "primary key; book identifier",
            "TITLE": "book title",
            "AUTHOR": "book author",
            "ISBN": "International Standard Book Number, if available",
            "CATEGORY": "book category or subject",
            "AVAILABLE_COPIES": "number of copies currently available",
        },
    },
    "LIBRARY_MEMBERS": {
        "description": "one row per registered library member",
        "columns": {
            "MEMBER_ID": "primary key; library member identifier",
            "MEMBER_NAME": "member full name",
            "EMAIL": "member email address",
            "PHONE": "member contact number",
        },
    },
    "BOOK_LOANS": {
        "description": "one row per book loan to a library member",
        "columns": {
            "LOAN_ID": "primary key; loan identifier",
            "BOOK_ID": "book identifier; references BOOKS.BOOK_ID",
            "MEMBER_ID": "member identifier; references LIBRARY_MEMBERS.MEMBER_ID",
            "ISSUE_DATE": "date the book was issued",
            "DUE_DATE": "date the book is due",
            "RETURN_DATE": "date returned; null if not yet returned",
        },
    },
}

# Additional domains requested for NLSQLAGENT.
# These entries describe the intended schema; they do not create Oracle tables.
SCHEMA.update({
    # Employees / HR
    "ATTENDANCE": {
        "description": "one row per employee attendance record",
        "columns": {
            "ATTENDANCE_ID": "primary key; attendance record identifier",
            "EMPLOYEE_ID": "employee identifier; references EMPLOYEES.EMPLOYEE_ID",
            "ATTENDANCE_DATE": "date of attendance",
            "CHECK_IN_TIME": "employee check-in timestamp or time value",
            "CHECK_OUT_TIME": "employee check-out timestamp or time value",
            "STATUS": "attendance status, such as present, absent, or half-day",
        },
    },
    "LEAVE_REQUESTS": {
        "description": "one row per employee leave request",
        "columns": {
            "LEAVE_REQUEST_ID": "primary key; leave request identifier",
            "EMPLOYEE_ID": "employee identifier; references EMPLOYEES.EMPLOYEE_ID",
            "LEAVE_TYPE": "type of leave requested",
            "START_DATE": "first date of leave",
            "END_DATE": "last date of leave",
            "STATUS": "request status, such as pending, approved, or rejected",
            "REASON": "employee-provided reason for leave",
        },
    },

    # Student management additions
    "FACULTY": {
        "description": "one row per faculty member or academic instructor",
        "columns": {
            "FACULTY_ID": "primary key; faculty identifier",
            "FACULTY_NAME": "faculty member full name",
            "EMAIL": "faculty member email address",
            "DEPARTMENT": "academic department",
            "SCHOOL_ID": "school identifier; references SCHOOLS.SCHOOL_ID",
        },
    },
    "EXAM_RESULTS": {
        "description": "one row per student's exam result",
        "columns": {
            "EXAM_RESULT_ID": "primary key; exam result identifier",
            "STUDENT_ID": "student identifier; references STUDENTS.STUDENT_ID",
            "COURSE_ID": "course identifier; references COURSES.COURSE_ID",
            "EXAM_NAME": "name or type of examination",
            "EXAM_DATE": "date of examination",
            "MARKS_OBTAINED": "marks earned by the student",
            "MAX_MARKS": "maximum possible marks",
            "GRADE": "grade awarded, if applicable",
        },
    },

    # Flights
    "AIRLINES": {
        "description": "one row per airline",
        "columns": {
            "AIRLINE_ID": "primary key; airline identifier",
            "AIRLINE_NAME": "airline name",
            "IATA_CODE": "two-character IATA airline code, if available",
            "COUNTRY": "airline home country",
        },
    },
    "AIRPORTS": {
        "description": "one row per airport",
        "columns": {
            "AIRPORT_ID": "primary key; airport identifier",
            "AIRPORT_CODE": "airport code, such as an IATA code",
            "AIRPORT_NAME": "airport name",
            "CITY": "airport city",
            "COUNTRY": "airport country",
        },
    },
    "FLIGHTS": {
        "description": "one row per scheduled flight service",
        "columns": {
            "FLIGHT_ID": "primary key; flight identifier",
            "AIRLINE_ID": "airline identifier; references AIRLINES.AIRLINE_ID",
            "FLIGHT_NUMBER": "airline flight number",
            "SOURCE_AIRPORT_ID": "origin airport; references AIRPORTS.AIRPORT_ID",
            "DESTINATION_AIRPORT_ID": "destination airport; references AIRPORTS.AIRPORT_ID",
            "DEPARTURE_TIME": "scheduled departure timestamp",
            "ARRIVAL_TIME": "scheduled arrival timestamp",
            "STATUS": "flight status, such as scheduled, delayed, or cancelled",
        },
    },
    "PASSENGERS": {
        "description": "one row per passenger profile used for travel bookings",
        "columns": {
            "PASSENGER_ID": "primary key; passenger identifier",
            "PASSENGER_NAME": "passenger full name",
            "EMAIL": "passenger email address",
            "PHONE": "passenger contact number",
            "PASSPORT_COUNTRY": "passport issuing country, if recorded",
        },
    },
    "FLIGHT_BOOKINGS": {
        "description": "one row per passenger flight booking",
        "columns": {
            "BOOKING_ID": "primary key; flight booking identifier",
            "PASSENGER_ID": "passenger identifier; references PASSENGERS.PASSENGER_ID",
            "FLIGHT_ID": "flight identifier; references FLIGHTS.FLIGHT_ID",
            "BOOKING_DATE": "date the flight booking was made",
            "SEAT_NUMBER": "assigned seat number, if available",
            "BOOKING_STATUS": "booking status, such as confirmed or cancelled",
            "TICKET_PRICE": "ticket price for this booking",
        },
    },

    # Railways
    "TRAINS": {
        "description": "one row per train service",
        "columns": {
            "TRAIN_ID": "primary key; train identifier",
            "TRAIN_NUMBER": "train number",
            "TRAIN_NAME": "train name",
            "TRAIN_TYPE": "train category, such as express or local",
        },
    },
    "STATIONS": {
        "description": "one row per railway station",
        "columns": {
            "STATION_ID": "primary key; station identifier",
            "STATION_CODE": "station code, if available",
            "STATION_NAME": "station name",
            "CITY": "station city",
            "STATE": "state or region where the station is located",
        },
    },
    "TRAIN_SCHEDULES": {
        "description": "one row per train stop in a train schedule",
        "columns": {
            "SCHEDULE_ID": "primary key; schedule row identifier",
            "TRAIN_ID": "train identifier; references TRAINS.TRAIN_ID",
            "STATION_ID": "station identifier; references STATIONS.STATION_ID",
            "ARRIVAL_TIME": "scheduled arrival time at this station",
            "DEPARTURE_TIME": "scheduled departure time from this station",
            "STOP_NUMBER": "station order in the train route",
            "DAY_NUMBER": "day offset for overnight journeys, if applicable",
        },
    },
    "TRAIN_RESERVATIONS": {
        "description": "one row per train seat reservation",
        "columns": {
            "RESERVATION_ID": "primary key; train reservation identifier",
            "TRAIN_ID": "train identifier; references TRAINS.TRAIN_ID",
            "PASSENGER_ID": "passenger identifier; references PASSENGERS.PASSENGER_ID",
            "SOURCE_STATION_ID": "boarding station; references STATIONS.STATION_ID",
            "DESTINATION_STATION_ID": "destination station; references STATIONS.STATION_ID",
            "TRAVEL_DATE": "date of train travel",
            "SEAT_NUMBER": "reserved seat number, if applicable",
            "RESERVATION_STATUS": "reservation status, such as confirmed or waitlisted",
            "FARE": "reservation fare",
        },
    },

    # Banking
    "BANK_ACCOUNTS": {
        "description": "one row per bank account",
        "columns": {
            "ACCOUNT_ID": "primary key; bank account identifier",
            "CUSTOMER_ID": "account holder; references CUSTOMERS.CUSTOMER_ID",
            "ACCOUNT_NUMBER": "bank account number; sensitive, avoid displaying in full",
            "ACCOUNT_TYPE": "account type, such as savings or current",
            "BALANCE": "current account balance",
            "ACCOUNT_STATUS": "account status, such as active or frozen",
            "OPENED_DATE": "date the account was opened",
        },
    },
    "BANK_TRANSACTIONS": {
        "description": "one row per bank account transaction",
        "columns": {
            "TRANSACTION_ID": "primary key; bank transaction identifier",
            "ACCOUNT_ID": "account identifier; references BANK_ACCOUNTS.ACCOUNT_ID",
            "TRANSACTION_DATE": "date and time of the transaction",
            "TRANSACTION_TYPE": "transaction type, such as deposit, withdrawal, or transfer",
            "AMOUNT": "transaction amount",
            "DESCRIPTION": "transaction description or reference",
            "TRANSACTION_STATUS": "transaction status",
        },
    },

    # E-commerce (separate from the existing sales/retail order tables)
    "ORDERS": {
        "description": "one row per e-commerce customer order",
        "columns": {
            "ORDER_ID": "primary key; e-commerce order identifier",
            "CUSTOMER_ID": "customer identifier; references CUSTOMERS.CUSTOMER_ID",
            "ORDER_DATE": "date and time the order was placed",
            "ORDER_STATUS": "order status, such as pending, paid, shipped, or cancelled",
            "SHIPPING_ADDRESS": "delivery address for the order",
            "TOTAL_AMOUNT": "total order amount",
        },
    },
    "ORDER_ITEMS": {
        "description": "one row per product line in an e-commerce order",
        "columns": {
            "ORDER_ITEM_ID": "primary key; order item identifier",
            "ORDER_ID": "order identifier; references ORDERS.ORDER_ID",
            "PRODUCT_ID": "product identifier; references PRODUCTS.PRODUCT_ID",
            "QUANTITY": "number of units ordered",
            "UNIT_PRICE": "unit price charged for the item",
        },
    },

    # Hotels
    "HOTELS": {
        "description": "one row per hotel or lodging property",
        "columns": {
            "HOTEL_ID": "primary key; hotel identifier",
            "HOTEL_NAME": "hotel name",
            "CITY": "city where the hotel is located",
            "ADDRESS": "hotel street address",
            "STAR_RATING": "hotel star rating, if applicable",
            "PHONE": "hotel contact number",
        },
    },
    "HOTEL_ROOMS": {
        "description": "one row per room in a hotel",
        "columns": {
            "ROOM_ID": "primary key; room identifier",
            "HOTEL_ID": "hotel identifier; references HOTELS.HOTEL_ID",
            "ROOM_NUMBER": "room number or label within the hotel",
            "ROOM_TYPE": "room type, such as single, double, or suite",
            "RATE_PER_NIGHT": "nightly room rate",
            "ROOM_STATUS": "room status, such as available or maintenance",
        },
    },
    "HOTEL_BOOKINGS": {
        "description": "one row per customer hotel room booking",
        "columns": {
            "HOTEL_BOOKING_ID": "primary key; hotel booking identifier",
            "CUSTOMER_ID": "customer identifier; references CUSTOMERS.CUSTOMER_ID",
            "HOTEL_ID": "hotel identifier; references HOTELS.HOTEL_ID",
            "ROOM_ID": "room identifier; references HOTEL_ROOMS.ROOM_ID",
            "CHECK_IN_DATE": "booking check-in date",
            "CHECK_OUT_DATE": "booking check-out date",
            "BOOKING_STATUS": "booking status, such as confirmed or cancelled",
            "TOTAL_AMOUNT": "total booking amount",
        },
    },

    # Transport and logistics
    "VEHICLES": {
        "description": "one row per vehicle used in transport or logistics",
        "columns": {
            "VEHICLE_ID": "primary key; vehicle identifier",
            "VEHICLE_TYPE": "vehicle type, such as van, truck, or car",
            "REGISTRATION_NUMBER": "vehicle registration number",
            "CAPACITY": "vehicle load or passenger capacity",
            "STATUS": "vehicle status, such as available or in service",
        },
    },
    "DRIVERS": {
        "description": "one row per driver",
        "columns": {
            "DRIVER_ID": "primary key; driver identifier",
            "DRIVER_NAME": "driver full name",
            "LICENSE_NUMBER": "driver licence number; sensitive identifier",
            "PHONE": "driver contact number",
            "DRIVER_STATUS": "driver status, such as active or inactive",
        },
    },
    "SHIPMENTS": {
        "description": "one row per shipment or delivery job",
        "columns": {
            "SHIPMENT_ID": "primary key; shipment identifier",
            "VEHICLE_ID": "assigned vehicle; references VEHICLES.VEHICLE_ID",
            "DRIVER_ID": "assigned driver; references DRIVERS.DRIVER_ID",
            "ORIGIN": "shipment origin location",
            "DESTINATION": "shipment destination location",
            "SHIPMENT_DATE": "date the shipment departed or was created",
            "DELIVERY_DATE": "actual or expected delivery date",
            "SHIPMENT_STATUS": "shipment status, such as pending, in transit, or delivered",
        },
    },
})



def schema_description(schema=SCHEMA):
    """Turn the schema into plain text for the AI prompt."""
    blocks = []
    for table, info in schema.items():
        lines = [f"Table: {table}", f"Description: {info['description']}", "Columns:"]
        width = max(len(column) for column in info["columns"])
        for column, meaning in info["columns"].items():
            lines.append(f"  {column.ljust(width)}  - {meaning}")
        blocks.append("\n".join(lines))
    return "\n\n".join(blocks)


if __name__ == "__main__":
    print(schema_description())
