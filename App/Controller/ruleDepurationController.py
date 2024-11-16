import pandas as pd
from PyQt6 import QtWidgets
import re
import json
import os
import smtplib
import dns.resolver
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import unidecode
from email_validator import validate_email, EmailNotValidError
from validate_email_address import validate_email as py3_validate_email
from difflib import get_close_matches


class RuleDepurationController:

    def __init__(self):
        self.created_rules_file = os.path.join(os.path.dirname(__file__), '..', 'Files', 'createdRules.JSON')
        self.custom_rules = self.load_custom_rules()
        self.mx_cache = {}  
        self.dns_timeout = 1  
        self.smtp_timeout = 1  
        self.max_threads = 10
        self.counter = 0
        self.common_domains = [
            'gmail.com',
            'hotmail.com',
            'outlook.com',
            'yahoo.com'
            'hotmail.es',
            'outlook.es',
            'yahoo.es',
        ]
        
        
    def load_custom_rules(self, parent_widget=None):    
        try:
            with open(self.created_rules_file, 'r') as file:
                rules = json.load(file)
                return rules
        except FileNotFoundError:
            self._show_error_message("No se encontró el archivo", parent_widget)
            return []

    
    def apply_rules(self, data, rules, parent_widget=None):

        for rule, column, params in rules:
            if column not in data.columns:
                self._show_column_error_message(column, parent_widget)
                continue

            if "Estandarizacion de Telefonos" in rule:
                data[column] = self._apply_phone_rules(data[column], params)
            elif "Estandarizacion de Cedulas" in rule:
                data[column] = self._apply_cedula_rules(data[column], params)
            elif "Validacion Correos" in rule:
                data[column] = data[column].apply(self._correct_common_domains)
                data[column] = self._apply_email_rules(data[column], params)
            elif "Eliminacion de Duplicados" in rule:
                data = self._handle_duplicates(data, column, params)
                
            else:
                data = self._apply_custom_rule(rule, data, column)

        return data
    
    def _apply_custom_rule(self, rule_name, data, column):
        normalized_rule_name = rule_name.strip().lower()
        common_imports = {
            "str": str,
            "re": re,
            "pd": pd,  
            "isinstance": isinstance,
            "unidecode": unidecode.unidecode,
            "__builtins__": {} 
        }

        for rule in self.custom_rules:
            if rule["rule_name"].strip().lower() == normalized_rule_name:
                rule_code = rule["code"]
                try:
                    exec(rule_code, common_imports, {"data": data, "column": column})
                except Exception as e:
                    self._show_error_message(f"Error al ejecutar la regla personalizada '{rule_name}': {e}")
                break
        else:
            self._show_error_message(f"No se encontró ninguna regla personalizada con el nombre '{rule_name}'")
        
        return data


    def _apply_cedula_rules(self, series, params):
        series = series.apply(lambda x: self._identify_and_apply_rules(x, params) if pd.notnull(x) else x)
        return series

    def _identify_and_apply_rules(self, id_number, params):
        id_type = self._identify_id_type(id_number)

        # Aplicar reglas específicas si es cédula de identidad
        if id_type == "cedula_identidad":
            # Aplicar normalización especial para eliminar ceros separadores en posiciones específicas
            id_number = self._normalize_cedula_identidad_with_zero_separator(id_number)

        # Aplicar reglas generales para todos los tipos de identificación
        if "Eliminar separador '-'" in params["modification"]:
            id_number = str(id_number).replace('-', '')

        if "Eliminar separador '0'" in params["modification"] and id_type == "cedula_identidad":
            id_number = self._normalize_cedula_identidad_with_zero_separator(id_number)

        if "Eliminar ambos separadores" in params["modification"]:
            id_number = str(id_number).replace('-', '')
            id_number = self._normalize_cedula_identidad_with_zero_separator(str(id_number).replace('-', '')) if id_type == "cedula_identidad" else str(id_number).replace('-', '')
            
        # Validar el formato de identificación
        if "Validar formato de cédula" in params["modification"]:
            user_friendly_format = params["modification"].split(":")[-1].strip()
            format_regex = self._convert_friendly_format_to_regex(user_friendly_format)
            id_number = id_number if re.fullmatch(format_regex, str(id_number)) else None

        # Convertir la identificación a un formato personalizado
        if "Convertir cédula a formato" in params["modification"]:
            custom_format = params["modification"].split(":")[-1].strip()
            id_number = self._convert_to_custom_format(str(id_number), custom_format, id_type)

        return id_number

    def _identify_id_type(self, id_number):
        """
        Identifica el tipo de identificación en función de su formato.
        """
        id_number = str(id_number)

        # Formatos de cédula de identidad (varias combinaciones con guiones y ceros separadores)
        if (re.fullmatch(r"\d{1}-\d{3}-\d{3}", id_number) or    # Formato x-xxx-xxx
            re.fullmatch(r"\d{1}-0\d{3}0\d{3}", id_number) or   # Formato x-0xxx0xxx
            re.fullmatch(r"\d{1}-0\d{3}-0\d{3}", id_number) or   # Formato x-0xxx-0xxx
            re.fullmatch(r"\d{1}-\d{6}", id_number) or          # Formato x-xxxxxx
            re.fullmatch(r"\d{7}", id_number) or                # Formato xxxxxxx (sin guiones ni ceros)
            re.fullmatch(r"\d0\d{3}0\d{3}", id_number) or       # Formato x0xxx0xxx
            re.fullmatch(r"\d{9,10}", id_number) or
            re.fullmatch(r"\d{1}-\d{8}", id_number)):        # Formato x0xxx0xxx
            return "cedula_identidad"
        
        # Formato de cédula de residencia (DIMEX) (11 o 12 dígitos sin guiones)
        elif re.fullmatch(r"\d{11,12}", id_number):
            return "cedula_residencia"
        
        # Formato de cédula jurídica (10 dígitos sin guiones)
        elif (re.fullmatch(r"\d{1}-\d{3}-\d{6}", id_number) or 
            re.fullmatch(r"\d{9,25}", id_number) or  
            re.fullmatch(r"\d{10}", id_number)):
            return "cedula_juridica"
        
        # Formato de NITE (10 dígitos sin guiones)
        elif (re.fullmatch(r"\d{1}-\d{3}-\d{6}", id_number) or   
            re.fullmatch(r"\d{10}", id_number)): 
            return "nite"
        
        # Formato de pasaporte (generalmente 6-9 caracteres alfanuméricos)
        elif (re.fullmatch(r"[A-Za-z]{1,2}\d{5,9}", id_number) or             # Letras seguidas de números (e.g., HK920921)
            re.fullmatch(r"[A-Za-z]{1,3}\d{6,9}", id_number) or    
            re.fullmatch(r"[A-Za-z]{1,3}\s?\d{6,9}", id_number) or          # Letras y números con espacio opcional (e.g., USA 537533907)
            re.fullmatch(r"[A-Za-z]{2}\d{9,13}", id_number)):               # Dos letras y hasta 13 dígitos (e.g., CR52147895645563)
            return "pasaporte"
        

        return "unknown"

    def _convert_friendly_format_to_regex(self, friendly_format):
        regex_pattern = ""

        for char in friendly_format:
            if char == '9':
                regex_pattern += r'\d'  
            else:
                regex_pattern += re.escape(char) 

        return regex_pattern

    def _convert_to_custom_format(self, id_number, custom_format, id_type):
        # Si es una cédula de identidad, aplica normalización especial antes de formatear
        if id_type == "cedula_identidad":
            id_number = self._normalize_cedula_identidad_with_zero_separator(id_number)
        
        formatted_regex = custom_format.replace("9", r"\d").replace("#", r"\d").replace("0", r"0")

        if re.fullmatch(formatted_regex, id_number):
            return id_number

        digits = ''.join(filter(str.isdigit, id_number))
        required_digits = custom_format.count('9') + custom_format.count('#')

        if len(digits) != required_digits:
            return None

        formatted_id = self._apply_custom_format(digits, custom_format)
        return formatted_id

    def _normalize_cedula_identidad_with_zero_separator(self, cedula):

        # Paso 1: Quitar todos los guiones
        cedula = cedula.replace('-', '')

        # Paso 2: Verificar si ahora tiene el formato x0xxx0xxx y eliminar ceros en posiciones específicas
        if re.match(r"^\d0\d{3}0\d{3}$", cedula):
            normalized_cedula = cedula[0] + cedula[2:5] + cedula[6:]
            
            return normalized_cedula

        # Paso 3: Otros formatos de cédula de identidad sin guiones (ej., x0xxxxxx o xxxxxxxx)
        # Si es un formato de 9 dígitos pero con ceros en posiciones específicas, elimina solo los ceros de esas posiciones
        if re.fullmatch(r"\d{9}", cedula) and cedula[1] == '0' and cedula[5] == '0':
            normalized_cedula = cedula[0] + cedula[2:5] + cedula[6:]
            return normalized_cedula

        # Si no cumple con los formatos anteriores, retornar la cédula sin modificaciones
        return cedula

  

    def _apply_custom_format(self, digits, custom_format):
        formatted_id = ""
        digit_index = 0

        for char in custom_format:
            if (char == "#" or char == "9") and digit_index < len(digits):
                formatted_id += digits[digit_index]
                digit_index += 1
            elif char == "0":
                formatted_id += "0"  
            else:
                formatted_id += char 

        return formatted_id if digit_index == len(digits) else None




    def _handle_duplicates(self, df, column, params, parent_widget=None):

        modification = params.get("modification", "")
        if "Eliminar duplicados generales" in modification:
            df = df.drop_duplicates()

        elif "Eliminar duplicados según las columnas" in modification:
            try:
                columns_text = modification.split(":")[1].strip()
                columns = [col.strip() for col in columns_text.split(",")]
                df = df.drop_duplicates(subset=columns)
            except IndexError:
                self._show_error_message("Error al extraer las columnas de la modificación", parent_widget)
        else:
            self._show_error_message("No se reconoció la modificación para eliminar duplicados", parent_widget)

        return df
    
    def _show_error_message(self, message, parent_widget=None):
        msg_box = QtWidgets.QMessageBox(parent_widget)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def _show_column_error_message(self, column, parent_widget=None):
        
        msg_box = QtWidgets.QMessageBox(parent_widget)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Error de columna")
        msg_box.setText(f'La columna "{column}" no existe en los datos.')
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg_box.exec()

    def _validate_emails(self, series):
        email_regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return series.apply(lambda x: x if re.match(email_regex, x) else "Correo invalido")

    def _apply_phone_rules(self, series, params):
        
        if "Validar longitud de los teléfonos" in params["modification"]:
            match = re.search(r"Longitud:\s*(\d+)", params["modification"])
            if match:
                length_str = match.group(1)
                try:
                    length = int(length_str)
                    series = series.apply(lambda x: x if pd.isnull(x) or len(''.join(filter(str.isdigit, str(x)))) == length else None)
                except ValueError as ve:
                    QtWidgets.QMessageBox.warning(None, "Error", f"Error al validar la longitud del teléfono: {ve}")
            else:
                QtWidgets.QMessageBox.warning(None, "Error", "No se pudo encontrar una longitud válida en los parámetros.")

        if "Convertir a nulo teléfonos con 0 o 00" in params["modification"]:
            series = series.apply(lambda x: None if x == "0" or x == "00" else x)

        if "Convertir a nulo si coincide con" in params["modification"]:
            custom_null_value = params["modification"].split("'")[1]

            if "Reemplazar valor con" in params["modification"]:
                replace_value = params["modification"].split("'")[3]  
                series = series.apply(lambda x: replace_value if str(x) == custom_null_value else x)
            else:
                series = series.apply(lambda x: None if str(x) == custom_null_value else x)

        if "Convertir a formato sin separadores" in params["modification"]:
            series = series.apply(lambda x: ''.join(filter(str.isdigit, str(x))) if pd.notnull(x) else x)

        if "Convertir a formato personalizado" in params["modification"]:
            custom_format = params["modification"].split(":")[-1].strip()
            series = series.apply(lambda x: self._apply_custom_phone_format(str(x), custom_format) if pd.notnull(x) else x)

        return series

    def _apply_custom_phone_format(self, phone, custom_format):
        phone_digits = ''.join(filter(str.isdigit, phone))
        
        required_digits = custom_format.count('#')
        if len(phone_digits) != required_digits:
            return None

        formatted_phone = ""
        digit_index = 0

        for char in custom_format:
            if char == "#" and digit_index < len(phone_digits):
                formatted_phone += phone_digits[digit_index]
                digit_index += 1
            else:
                formatted_phone += char

        return formatted_phone

    def _show_column_error_message(self, column, parent_widget=None):

        msg_box = QtWidgets.QMessageBox(parent_widget)
        msg_box.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Error de columna")
        msg_box.setText(f'La columna "{column}" no existe en los datos.')
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
        msg_box.exec()
        
    def _remove_duplicates(self, df, column):
        return df.drop_duplicates(subset=[column])
    
    def _apply_email_rules(self, series, params):
        
        if "Convertir correos a minúsculas" in params["modification"]:
            series = series.str.lower()
            
        if "Dominios permitidos" in params["modification"]:
            allowed_domains = params["modification"].split(": ")[1].split(", ")
            series = self._validate_allowed_domains(series, allowed_domains)
            
        if "Validar correos con separadores" in params["modification"]:
            if "Separador personalizado" in params["modification"]:
                custom_separator = params["modification"].split(": ")[1]
                series = self._validate_email_separators(series, "Separador personalizado", custom_separator)
            else:
                
                if "coma" in params["modification"]:
                    selected_separator = ","
                elif "punto y coma" in params["modification"]:
                    selected_separator = ";"
                elif "barra" in params["modification"]:
                    selected_separator = "/"
                else:
                    selected_separator = "No seleccionado"  
                
                series = self._validate_email_separators(series, selected_separator)
        
        if "Validar formato de correo" in params["modification"]:
            match = re.search(r"Inválidos como '([^']+)'", params["modification"])
            invalid_value = match.group(1) if match else "null"
            series = self._validate_email_format_per_email(series, invalid_value)
            series = self._validate_email_for_common_domains(series, invalid_value)  
            
        return series
    
    def _correct_common_domains(self, email):
        try:
            local_part, domain = email.split('@')
            matched_domain = get_close_matches(domain.lower(), self.common_domains, n=1, cutoff=0.8)
            if matched_domain:
                corrected_domain = matched_domain[0]
                return f"{local_part}@{corrected_domain}"
            return email
        except ValueError:
            return email  
        
    def _validate_email_format_per_email(self, series, invalid_value):
        return series.apply(lambda email: self._process_email_string_for_format(email, invalid_value))

    def _process_email_string_for_format(self, email_string, invalid_value):
        emails, separator = self._split_email_string(email_string)
        validated_emails = [self._validate_single_email_format(email, invalid_value) for email in emails]
        return separator.join(validated_emails) if separator else validated_emails[0]

    def _split_email_string(self, email_string):
        separators = [',', ';', '/']
        for sep in separators:
            if sep in email_string:
                return [email.strip() for email in email_string.split(sep)], sep
        return [email_string], None 

    def _validate_single_email_format(self, email, invalid_value):
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        if email == "Correo invalido":
            return email
        return email if re.match(email_regex, email) else invalid_value

    def _validate_email_format(self, series):
        email_regex = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
        return series.apply(lambda x: x if re.match(email_regex, x) else "Formato invalido")

    def _validate_allowed_domains(self, series, allowed_domains):
        def is_valid_domain(email):
            domain = email.split('@')[-1] if '@' in email else None
            return email if domain in allowed_domains else "Dominio invalido"
        
        return series.apply(is_valid_domain)

    def _validate_email_separators(self, series, separator_type, custom_separator=None):

        separator = self._determine_separator(separator_type, custom_separator)
        validated_series = series.apply(lambda email_string: self._process_email_string(email_string, separator))
        
        return validated_series

    def _determine_separator(self, separator_type, custom_separator):
        
        if separator_type == "Separador personalizado" and custom_separator:
            return custom_separator
        elif separator_type == ",":
            return ','
        elif separator_type == ";":
            return ';'
        elif separator_type == "/":
            return '/'
        else:
            return 'No seleccionado'  


    def _process_email_string(self, email_string, separator):
        if separator not in email_string:
            return email_string  

        emails = self._split_emails(email_string, separator)
        validated_emails = self._validate_each_email(emails)
        
        return separator.join(validated_emails)

    def _split_emails(self, email_string, separator):
        return [email.strip() for email in email_string.split(separator)]

    def _validate_each_email(self, emails):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        
        validated_emails = []
        for email in emails:
            if re.match(email_pattern, email):
                validated_emails.append(email)
            else:
                validated_emails.append("Correo invalido")
        return validated_emails

    def _validate_email_for_common_domains(self, series, invalid_value):
        validated_series = []
        for email_string in series:
            emails, separator = self._split_email_string(email_string)
            total_emails = len(emails)
            validated_emails = [None] * total_emails
            with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
                future_to_email = {
                    executor.submit(self._validate_email, email, invalid_value): (idx, email)
                    for idx, email in enumerate(emails)
                }

                for future in as_completed(future_to_email):
                    original_idx, email = future_to_email[future]
                    try:
                        result = future.result()
                        validated_emails[original_idx] = result
                    except Exception:
                        validated_emails[original_idx] = invalid_value

            validated_series.append(separator.join(validated_emails) if separator else validated_emails[0])

        return pd.Series(validated_series)


    def _validate_email(self, email, invalid_value):
        self.counter += 1
        try:
            v = validate_email(email)  
            validated_email = v["email"]  
            domain = email.split('@')[-1]

            mx_passed = self._validate_mx_and_dns(domain)
            if not mx_passed:
                return invalid_value  

            smtp_passed = self._validate_smtp(email, domain)
            if not smtp_passed:
                return invalid_value
            
            spf_passed = self._validate_spf(domain)
            if not spf_passed and not smtp_passed:
                return invalid_value  

            dmarc_passed = self._validate_dmarc(domain)
            if not dmarc_passed and not smtp_passed:
                return invalid_value  

            return validated_email  

        except EmailNotValidError:
            return invalid_value  


    def _validate_mx_and_dns(self, domain):

        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            if not mx_records:
                return False  
            return True  
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False  
        
    def _validate_spf(self, domain):
        try:
            spf_record = dns.resolver.resolve(f'{domain}', 'TXT')
            for rdata in spf_record:
                if 'v=spf1' in str(rdata):
                    return True  
            return False  
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False

    def _validate_dmarc(self, domain):
        try:
            dmarc_record = dns.resolver.resolve(f'_dmarc.{domain}', 'TXT')
            if any('v=DMARC1' in str(rdata) for rdata in dmarc_record):
                return True 
            else:
                return False  
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN):
            return False  

    def _validate_smtp(self, email, domain):
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            mx_record = str(mx_records[0].exchange) 
            with smtplib.SMTP(mx_record, timeout=self.smtp_timeout) as server:
                server.set_debuglevel(0)  
                server.helo()  
                server.mail('no-reply@mydomain.com')  
                code, _ = server.rcpt(email)  
                if code == 250:
                    return True
                return False  
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected, smtplib.SMTPRecipientsRefused) as e:
            return False  
        except Exception as e:
            return False  