from __future__ import unicode_literals
from datetime import datetime

from django.db import models


class AiVirtuemartCategories(models.Model):
    virtuemart_category_id = models.IntegerField(primary_key=True)
    virtuemart_vendor_id = models.IntegerField(default=1)
    category_template = models.CharField(max_length=128L, blank=True)
    category_layout = models.CharField(max_length=64L, blank=True)
    category_product_layout = models.CharField(max_length=64L, blank=True)
    products_per_row = models.IntegerField(null=True, blank=True)
    limit_list_step = models.CharField(max_length=32L, blank=True)
    limit_list_initial = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(default=0)
    metarobot = models.CharField(max_length=40L)
    metaauthor = models.CharField(max_length=64L)
    ordering = models.IntegerField(default=0)
    shared = models.IntegerField(default=0)
    published = models.IntegerField(default=1)
    created_on = models.DateTimeField(default=datetime.now())
    created_by = models.IntegerField(default=1)
    modified_on = models.DateTimeField(default=datetime.now())
    modified_by = models.IntegerField(default=1)
    locked_on = models.DateTimeField(default=datetime.now())
    locked_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_categories'


class AiVirtuemartCategoriesRuRu(models.Model):
    virtuemart_category_id = models.IntegerField(primary_key=True)
    category_name = models.CharField(max_length=180L)
    category_description = models.CharField(max_length=19000L)
    metadesc = models.CharField(max_length=400L)
    metakey = models.CharField(max_length=400L)
    customtitle = models.CharField(max_length=255L)
    slug = models.CharField(max_length=192L, unique=True)

    class Meta:
        db_table = 'ai_virtuemart_categories_ru_ru'


class AiVirtuemartCategoryCategories(models.Model):
    id = models.IntegerField(primary_key=True)
    category_parent_id = models.IntegerField()
    category_child_id = models.IntegerField()
    ordering = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_category_categories'


class AiVirtuemartCategoryMedias(models.Model):
    id = models.IntegerField(primary_key=True)
    virtuemart_category_id = models.IntegerField()
    virtuemart_media_id = models.IntegerField()
    ordering = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_category_medias'


class AiVirtuemartManufacturers(models.Model):
    virtuemart_manufacturer_id = models.IntegerField(primary_key=True)
    virtuemart_manufacturercategories_id = models.IntegerField(null=True, blank=True)
    hits = models.IntegerField(default=0)
    published = models.IntegerField(default=1)
    created_on = models.DateTimeField(default=datetime.now())
    created_by = models.IntegerField(default=1)
    modified_on = models.DateTimeField(default=datetime.now())
    modified_by = models.IntegerField(default=1)
    locked_on = models.DateTimeField(default=datetime.now())
    locked_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_manufacturers'


class AiVirtuemartManufacturersRuRu(models.Model):
    virtuemart_manufacturer_id = models.IntegerField(primary_key=True)
    mf_name = models.CharField(max_length=180L)
    mf_email = models.CharField(max_length=255L)
    mf_desc = models.CharField(max_length=19000L)
    mf_url = models.CharField(max_length=255L)
    slug = models.CharField(max_length=192L, unique=True)

    class Meta:
        db_table = 'ai_virtuemart_manufacturers_ru_ru'


class AiVirtuemartMedias(models.Model):
    virtuemart_media_id = models.IntegerField(primary_key=True)
    virtuemart_vendor_id = models.IntegerField(default=1)
    file_title = models.CharField(max_length=126L, blank=True)
    file_description = models.CharField(max_length=254L, blank=True)
    file_meta = models.CharField(max_length=254L)
    file_mimetype = models.CharField(max_length=64L, default="image/jpeg")
    file_type = models.CharField(max_length=32L, default="product")
    file_url = models.CharField(max_length=900L)
    file_url_thumb = models.CharField(max_length=900L)
    file_is_product_image = models.IntegerField(default=1)
    file_is_downloadable = models.IntegerField(default=0)
    file_is_forsale = models.IntegerField(db_column='file_is_forSale', default=0) # Field name made lowercase.
    file_params = models.CharField(max_length=17500L)
    file_lang = models.CharField(max_length=500L)
    shared = models.IntegerField(default=0)
    published = models.IntegerField(default=1)
    created_on = models.DateTimeField(default=datetime.now())
    created_by = models.IntegerField(default=1)
    modified_on = models.DateTimeField(default=datetime.now())
    modified_by = models.IntegerField(default=1)
    locked_on = models.DateTimeField(default=datetime.now())
    locked_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_medias'


class AiVirtuemartProductCategories(models.Model):
    id = models.IntegerField(primary_key=True)
    virtuemart_product_id = models.IntegerField()
    virtuemart_category_id = models.IntegerField()
    ordering = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_product_categories'


class AiVirtuemartProductCustomfields(models.Model):
    virtuemart_customfield_id = models.IntegerField(primary_key=True)
    virtuemart_product_id = models.IntegerField()
    virtuemart_custom_id = models.IntegerField()
    custom_value = models.CharField(max_length=8000L, blank=True)
    custom_price = models.DecimalField(null=True, max_digits=17, decimal_places=5, blank=True)
    custom_param = models.CharField(max_length=12800L, blank=True)
    published = models.IntegerField(default=1)
    created_on = models.DateTimeField(default=datetime.now())
    created_by = models.IntegerField(default=1)
    modified_on = models.DateTimeField(default=datetime.now())
    modified_by = models.IntegerField(default=1)
    locked_on = models.DateTimeField(default=datetime.now())
    locked_by = models.IntegerField(default=0)
    ordering = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_product_customfields'


class AiVirtuemartProductManufacturers(models.Model):
    id = models.IntegerField(primary_key=True)
    virtuemart_product_id = models.IntegerField(null=True, blank=True)
    virtuemart_manufacturer_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'ai_virtuemart_product_manufacturers'


class AiVirtuemartProductMedias(models.Model):
    id = models.IntegerField(primary_key=True)
    virtuemart_product_id = models.IntegerField()
    virtuemart_media_id = models.IntegerField()
    ordering = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_product_medias'


class AiVirtuemartProductPrices(models.Model):
    virtuemart_product_price_id = models.IntegerField(primary_key=True)
    virtuemart_product_id = models.IntegerField()
    virtuemart_shoppergroup_id = models.IntegerField(null=True, blank=True)
    product_price = models.DecimalField(null=True, max_digits=17, decimal_places=5, blank=True)
    override = models.IntegerField(null=True, blank=True)
    product_override_price = models.DecimalField(null=True, max_digits=17, decimal_places=5, blank=True)
    product_tax_id = models.IntegerField(null=True, blank=True)
    product_discount_id = models.IntegerField(null=True, blank=True)
    product_currency = models.IntegerField(null=True, blank=True)
    product_price_publish_up = models.DateTimeField(null=True, blank=True)
    product_price_publish_down = models.DateTimeField(null=True, blank=True)
    price_quantity_start = models.IntegerField(null=True, blank=True)
    price_quantity_end = models.IntegerField(null=True, blank=True)
    created_on = models.DateTimeField(default=datetime.now())
    created_by = models.IntegerField(default=1)
    modified_on = models.DateTimeField(default=datetime.now())
    modified_by = models.IntegerField(default=1)
    locked_on = models.DateTimeField(default=datetime.now())
    locked_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_product_prices'


class AiVirtuemartProducts(models.Model):
    virtuemart_product_id = models.IntegerField(primary_key=True)
    virtuemart_vendor_id = models.IntegerField(default=1)
    product_parent_id = models.IntegerField(default=0)
    product_sku = models.CharField(max_length=64L, blank=True)
    product_gtin = models.CharField(max_length=64L, blank=True)
    product_mpn = models.CharField(max_length=64L, blank=True)
    product_weight = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    product_weight_uom = models.CharField(max_length=7L, blank=True)
    product_length = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    product_width = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    product_height = models.DecimalField(null=True, max_digits=12, decimal_places=4, blank=True)
    product_lwh_uom = models.CharField(max_length=7L, blank=True)
    product_url = models.CharField(max_length=255L, blank=True)
    product_in_stock = models.IntegerField(default=0)
    product_ordered = models.IntegerField(default=0)
    low_stock_notification = models.IntegerField(default=0)
    product_available_date = models.DateTimeField(default=datetime.now())
    product_availability = models.CharField(max_length=32L, blank=True)
    product_special = models.IntegerField(null=True, blank=True)
    product_sales = models.IntegerField(default=0)
    product_unit = models.CharField(max_length=8L, blank=True)
    product_packaging = models.DecimalField(null=True, max_digits=9, decimal_places=4, blank=True)
    product_params = models.CharField(max_length=2000L)
    hits = models.IntegerField(null=True, blank=True)
    intnotes = models.CharField(max_length=18000L, blank=True)
    metarobot = models.CharField(max_length=400L, blank=True)
    metaauthor = models.CharField(max_length=400L, blank=True)
    layout = models.CharField(max_length=16L, blank=True)
    published = models.IntegerField(default=1)
    pordering = models.IntegerField(default=0)
    created_on = models.DateTimeField(default=datetime.now())
    created_by = models.IntegerField(default=0)
    modified_on = models.DateTimeField(default=datetime.now())
    modified_by = models.IntegerField(default=0)
    locked_on = models.DateTimeField(default=datetime.now())
    locked_by = models.IntegerField(default=0)

    class Meta:
        db_table = 'ai_virtuemart_products'


class AiVirtuemartProductsRuRu(models.Model):
    virtuemart_product_id = models.IntegerField(primary_key=True)
    product_s_desc = models.CharField(max_length=2000L, default="")
    product_desc = models.CharField(max_length=18400L)
    product_name = models.CharField(max_length=180L)
    metadesc = models.CharField(max_length=400L)
    metakey = models.CharField(max_length=400L)
    customtitle = models.CharField(max_length=255L)
    slug = models.CharField(max_length=192L, unique=True)

    class Meta:
        db_table = 'ai_virtuemart_products_ru_ru'