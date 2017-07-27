class UserTokenTypes:
  REGISTRATION = 'RG'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]


class MediaTypes:
  EXPERTISE_REPORT = 'ER'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]


class AuctionStates:
  YENI_GELEN = 'YG'
  ONAY_BEKLEYEN = 'OB'
  TAMAMLANAN = 'TM'
  COP_KUTUSU = 'CK'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]


class SellerTypes:
  BANKA = 'BN'
  SAHIBINDEN = 'SH'
  SIRKETTEN = 'SR'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]


class DeedInfos:
  ARSA_TAPUSU = 'AT'
  CINS_TASHIHI = 'CT'
  KAT_IRTIFAKI = 'KI'
  KAT_MULKIYETI = 'KM'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]


class PropertyCategories:
  ARSA = 'AR'
  KONUT = 'KO'
  TICARI = 'TI'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]


class PropertyTypes:
  BAG_BAHCE = 'BA'
  IMARLI = 'IM'
  TARLA = 'TA'
  BINA = 'BI'
  DAIRE = 'DA'
  MUSTAKIL = 'MU'
  DEPO = 'DE'
  DUKKAN = 'DU'
  FABRIKA = 'FA'
  OFIS = 'OF'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]


class ExpertiseRequestStates:
  YENI_GELEN = 'YG'
  GORUSME_ASAMASI = 'GA'
  ESLESEN = 'ES'
  COP_KUTUSU = 'CK'

  class Meta:
    max_length = 2
    choice_type = [str, unicode]

