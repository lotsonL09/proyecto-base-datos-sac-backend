from fastapi_mail import FastMail,ConnectionConfig,MessageSchema,MessageType
from config.config import settings
from fastapi import HTTPException,status
from entities.user import User_DB
from itsdangerous import URLSafeTimedSerializer

def make_email_html(user:User_DB):
    body=f"""
<td align="center" class="esd-stripe">
  <table bgcolor="#ffffff" align="center" cellpadding="0" cellspacing="0" width="600" class="es-content-body">
    <tbody>
      <tr>
        <td align="left" class="esd-structure es-p30t es-p20b es-p20r es-p20l es-m-p20t">
          <table cellpadding="0" cellspacing="0" width="100%">
            <tbody>
              <tr>
                <td width="560" align="center" valign="top" class="esd-container-frame">
                  <table cellpadding="0" cellspacing="0" width="100%">
                    <tbody>
                      <tr>
                        <td align="center" class="esd-block-text es-p10b">
                          <h1 class="es-m-txt-c" style="font-size:46px;line-height:100%">
                            ¡Bienvenido al Laboratorio de Sistemas Automáticos de Control!
                          </h1>
                        </td>
                      </tr>
                      <tr>
                        <td align="center" class="esd-block-image es-p10t es-p10b" style="font-size:0px">
                          <a target="_blank">
                            <img src="https://elrbbpo.stripocdn.email/content/guids/CABINET_6dfdad7857396b4e26660c822937c1f5261a6890bf76dc2a37000c1c06fed99f/images/fotos_sac_cropped.jpeg" alt="" width="530" class="adapt-img" style="display:block">
                          </a>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
      <tr>
        <td align="left" class="esd-structure es-p10t es-p10b es-p20r es-p20l">
          <table cellpadding="0" cellspacing="0" width="100%">
            <tbody>
              <tr>
                <td width="560" valign="top" align="center" class="es-m-p0r esd-container-frame">
                  <table cellspacing="0" width="100%" cellpadding="0">
                    <tbody>
                      <tr>
                        <td align="left" class="esd-block-text es-text-2441">
                          <p class="es-text-mobile-size-18" style="text-align:justify;font-size:18px;line-height:120%">
                              ​
                          </p>
                          <p class="es-text-mobile-size-18" style="text-align:justify;font-size:18px;line-height:120%">
                            Hola {user.first_name + " " +user.last_name},
                          </p>
                          <p style="line-height:120%">
                            ​
                          </p>
                          <p class="es-text-mobile-size-18" style="line-height:120%;font-size:18px">
                            ¡Nos llena de entusiasmo darte la bienvenida al Laboratorio de Sistemas Automáticos de Control! Estamos encantados de tenerte con nosotros como {user.role.value}.
                          </p>
                          <p class="es-text-mobile-size-18" style="line-height:120%;font-size:18px">
                            ​
                          </p>
                          <p class="es-text-mobile-size-18" style="font-size:18px;line-height:120%">
                            En el laboratorio, conocido con cariño como <em>"El Mítico"</em>, creemos firmemente que el respeto, el trabajo en equipo, la innovación y la constancia son esenciales para alcanzar nuestros objetivos. No solo buscamos el éxito en el ámbito profesional, sino también fomentar tu crecimiento personal.
                          </p>
                          <p class="es-text-mobile-size-18" style="line-height:120%;font-size:18px">
                            ​
                          </p>
                          <p class="es-text-mobile-size-18" style="line-height:120%;font-size:18px">
                            Queremos que te sientas en total confianza para proponer ideas, hacer preguntas y aprender de cada experiencia. Este espacio ha sido el punto de partida para muchas personas extraordinarias, quienes, como tú, comenzaron llenas de expectativas y hoy son parte del legado que le ha dado al laboratorio su prestigio dentro de la UDEP y más allá. No tenemos dudas de que tú también contribuirás de manera especial a nuestra historia.
                          </p>
                          <p class="es-text-mobile-size-18" style="line-height:120%;font-size:18px">
                            ​
                          </p>
                          <p class="es-text-mobile-size-18" style="font-size:18px;line-height:120%">
                            Esperamos que tu estancia aquí sea inolvidable y que el ritmo de SAC te impulse a alcanzar tus metas.
                          </p>
                          <p class="es-text-mobile-size-18" style="font-size:18px;line-height:120%">
                            ​
                          </p>
                          <p class="es-text-mobile-size-18" style="text-align:justify;font-size:18px;line-height:120%">
                            Saludos cordiales,
                          </p>
                          <p class="es-text-mobile-size-18" style="font-size:18px">
                            ​
                          </p>
                          <p class="es-text-mobile-size-18" style="font-size:18px">
                            William Ipanaqué y William Macalupú
                          </p>
                          <p>
                            ​
                          </p>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </td>
              </tr>
            </tbody>
          </table>
        </td>
      </tr>
    </tbody>
  </table>
</td>
"""
    return body

mail_config=ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=settings.USE_CREDENTIALS,
    VALIDATE_CERTS=settings.VALIDATE_CERTS
)

mail=FastMail(
    config=mail_config
)

def create_message(recipients:list[str],subject:str,body:str):
    message=MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )
    
    return message

serializer=URLSafeTimedSerializer(
        secret_key=settings.SECRET_KEY,
        salt="email-configuration"
    )

def create_url_safe_token(data:dict):
    
    token=serializer.dumps(obj=data)
    
    return token

def decode_url_safe_token(token:str):
    try:
        token_data=serializer.loads(token)
        return token_data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT)
