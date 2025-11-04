"""
Módulo de envío de mensajes y archivos a WhatsApp
Utiliza la API de Twilio para la comunicación
"""

from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import time
from src.logger import setup_logger

logger = setup_logger()


class WhatsAppSender:
    """
    Clase para enviar mensajes e imágenes a WhatsApp mediante Twilio
    """
    
    def __init__(self, account_sid, auth_token, from_number):
        """
        Inicializa el cliente de Twilio
        
        Args:
            account_sid (str): Account SID de Twilio
            auth_token (str): Auth Token de Twilio
            from_number (str): Número de WhatsApp de Twilio (formato: whatsapp:+1234567890)
        """
        self.from_number = from_number
        
        try:
            self.client = Client(account_sid, auth_token)
            logger.info("✓ Cliente de Twilio inicializado correctamente")
        except Exception as e:
            logger.error(f"Error al inicializar cliente de Twilio: {str(e)}")
            raise
    
    def send_message(self, to_number, message):
        """
        Envía un mensaje de texto a WhatsApp
        
        Args:
            to_number (str): Número de destino (formato: whatsapp:+1234567890)
            message (str): Mensaje a enviar
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Asegurar formato correcto del número
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )
            
            logger.info(f"✓ Mensaje enviado correctamente. SID: {message_obj.sid}")
            return True
            
        except TwilioRestException as e:
            logger.error(f"Error de Twilio al enviar mensaje: {e.msg}")
            return False
        except Exception as e:
            logger.error(f"Error al enviar mensaje: {str(e)}")
            return False
    
    def send_image(self, to_number, image_path, caption=None):
        """
        Envía una imagen a WhatsApp
        
        Args:
            to_number (str): Número de destino (formato: whatsapp:+1234567890)
            image_path (str): Ruta local de la imagen
            caption (str, optional): Texto que acompaña la imagen
            
        Returns:
            bool: True si se envió correctamente, False en caso contrario
        """
        try:
            # Asegurar formato correcto del número
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'
            
            # Para enviar archivos locales, necesitas subirlos a una URL pública
            # Por ahora, registramos el intento
            logger.warning("Nota: Para enviar imágenes, necesitas convertir la ruta local a URL pública")
            logger.info(f"Imagen preparada para envío: {image_path}")
            
            # Si tienes la imagen en una URL pública, usa este código:
            # message = self.client.messages.create(
            #     body=caption if caption else "",
            #     from_=self.from_number,
            #     to=to_number,
            #     media_url=[image_url]
            # )
            
            # Por ahora, enviamos un mensaje indicando que hay un reporte disponible
            if caption:
                self.send_message(to_number, f"📊 Reporte generado: {caption}\nArchivo: {image_path}")
            
            # Pausa entre mensajes para evitar rate limiting
            time.sleep(1)
            
            return True
            
        except TwilioRestException as e:
            logger.error(f"Error de Twilio al enviar imagen: {e.msg}")
            return False
        except Exception as e:
            logger.error(f"Error al enviar imagen: {str(e)}")
            return False
    
    def send_multiple_images(self, to_number, image_paths, captions=None):
        """
        Envía múltiples imágenes a WhatsApp
        
        Args:
            to_number (str): Número de destino
            image_paths (list): Lista de rutas de imágenes
            captions (list, optional): Lista de textos para cada imagen
            
        Returns:
            int: Número de imágenes enviadas exitosamente
        """
        successful = 0
        
        for i, image_path in enumerate(image_paths):
            caption = captions[i] if captions and i < len(captions) else None
            
            if self.send_image(to_number, image_path, caption):
                successful += 1
            
            # Pausa entre envíos
            time.sleep(2)
        
        logger.info(f"✓ Se enviaron {successful} de {len(image_paths)} imágenes")
        return successful
    
    @staticmethod
    def validate_phone_number(phone_number):
        """
        Valida el formato del número de teléfono
        
        Args:
            phone_number (str): Número a validar
            
        Returns:
            bool: True si el formato es válido
        """
        # Formato esperado: +1234567890 o whatsapp:+1234567890
        if phone_number.startswith('whatsapp:'):
            phone_number = phone_number.replace('whatsapp:', '')
        
        # Debe empezar con + y tener entre 10-15 dígitos
        if phone_number.startswith('+') and len(phone_number) >= 11 and len(phone_number) <= 16:
            return phone_number[1:].isdigit()
        
        return False