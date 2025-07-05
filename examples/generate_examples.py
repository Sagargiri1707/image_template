
"""
Example script demonstrating how to use the Dolze Templates library.

This script shows how to:
1. Load templates from JSON files
2. Render templates with different data
3. Save the generated images
"""

from cgitb import text
import os
import json
from datetime import datetime
from pathlib import Path

# Add parent directory to path so we can import the package
import sys

sys.path.append(str(Path(__file__).parent.parent))

from dolze_image_templates import (
    TemplateRegistry,
    get_template_registry,
    configure,
    get_font_manager,
)

# Initialize font manager to scan for fonts
font_manager = get_font_manager()
print("Font manager initialized. Available fonts:", font_manager.list_fonts())

# Configure the library
configure(
    templates_dir=os.path.join(
        os.path.dirname(__file__), "..", "dolze_image_templates", "templates"
    ),
    output_dir=os.path.join(os.path.dirname(__file__), "output"),
)


def generate_business_template(templateName: str):
    """Generate a business template post."""
    # Get the template registry
    registry = get_template_registry()
    template_data = {
        "cta_text": "LEARN MORE",
        "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
        "image_url": "https://images.pexels.com/photos/235986/pexels-photo-235986.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2",
        "cta_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",
        "heading": "plan your day in a snap",
        "subheading": "Driving success",
        "contact_email": "contact@business.com",
        "contact_phone": "+1-800-555-1234",
        "website_url": "dolze.ai /download",
        "quote": "The only way to do great work is to love what you do.",
        "theme_color": "#44EC9D",
        "user_avatar": "https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
        "user_name": "Alex Johnson",
        "user_title": "Marketing Director, TechCorp",
        "testimonial_text": "This product has completely transformed how we works. The intuitive interface and powerful features have saved us countless hours.",
    }
    # Template data mapping
    if templateName == "calendar_app_promo":
        template_data = {
            "cta_text": "LEARN MORE",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "image_url": "https://www.calendar.com/wp-content/uploads/2019/09/CalendarAndroidApp.png.webp",
            "cta_image": "https://images.unsplash.com/photo-1556742049-0cfed4f6a45d",
            "heading": "plan your day in a snap",
            "subheading": "Driving your success forward",
            "contact_email": "contact@business.com",
            "contact_phone": "+1-800-555-1234",
            "website_url": "dolze.ai/download",
            "quote": "The only way to do great work is to love what you do.",
            "theme_color": "#44EC9D",
            "user_avatar": "https://img.freepik.com/free-vector/blue-circle-with-white-user_78370-4707.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "user_name": "Alex Johnson",
            "user_title": "Marketing Director, TechCorp",
            "testimonial_text": "This product has completely transformed how we works. The intuitive interface and powerful features have saved us countless hours.",
        }
    elif templateName == "testimonials_template":
        template_data = {
            # Common fields
            "theme_color": "#44EC9D",
            "website_url": "dolze.ai/download",
            # Testimonials specific
            "user_avatar": "https://img.freepik.com/free-vector/isolated-young-handsome-man-different-poses-white-background-illustration_632498-859.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "user_name": "Sarah Johnson",
            "user_title": "Verified Buyer",
            "testimonial_text": "This product has completely transformed how we works. The intuitive interface and powerful features have saved us countless hours.",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
        }
    elif templateName == "blog_post" or templateName == "blog_post_2":
        template_data = {
            "theme_color": "#44EC9D",
            "website_url": "website.com/blog",
            "title": "How to be environment conscious without being weird",
            "author": "@username",  # to be inserted by db
            "read_time": "4",
            "publish_date": "2025-06-22",
            "excerpt": "This si a short description of the blog post. this is to be inserted by db and will be used to display the blog post in the feed",
            "image_url": "https://img.freepik.com/free-vector/underwater-ocean-reef-coral-background_107791-1853.jpg",
            "logo_url": "https://img.freepik.com/free-vector/gradient-s-letter-logo_343694-1365.jpg",
        }
    elif (
        templateName == "qa_template"
        or templateName == "qa_template_2"
        or templateName == "qa_template_3"
    ):
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "question": "What is Title?",
            "answer": "One wind turbine can produce enough electricity to power around 1,500 homes annually!",
            "username": "@username",
            "theme_color": "#44EC9D",
            "website_url": "website.com/blog",
        }
    elif  templateName == "quote_template_2":
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg",
            "quote1": "The only way to do",
            "quote2": "great work is to love what you do",
            "username": "@stevejobs",
            "website_url": "www.example.com",
            "theme_color": "#44EC9D",
        }
    elif templateName == "education_info" or templateName == "education_info_2":
        template_data = {
            "theme_color": "#44EC9D",
            "website_url": "website.com/blog",
            "product_name": "Product Name",
            "product_info": "One wind turbine can produce enough electricity to power around 1,500 homes annually!",
            "author": "@username",  # to be inserted by db
            "read_time": "4",
            "image_url": "https://img.freepik.com/free-photo/portrait-young-businesswoman-holding-eyeglasses-hand-against-gray-backdrop_23-2148029483.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "logo_url": "https://img.freepik.com/free-vector/gradient-s-letter-logo_343694-1365.jpg",
        }
    elif templateName == "product_promotion_2":
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?w=200&h=200&white=true",
            "image_url": "https://media.licdn.com/dms/image/v2/D4D12AQGnbgq78a4LMg/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1677634984855?e=1755734400&v=beta&t=PS0JBTOx91C-z1Tb4Ky4NOnQeRosuW-7i1GIDUj088o",
            "quote1": "the kanban board",
            "quote2": "you'll absolutely love",
            "theme_color": "#44EC9D",
            "website_url": "dolze.ai/download",
        }
    elif templateName == "product_promotion":
        template_data = {
            "image_url": "https://media.licdn.com/dms/image/v2/D4D12AQGnbgq78a4LMg/article-cover_image-shrink_720_1280/article-cover_image-shrink_720_1280/0/1677634984855?e=1755734400&v=beta&t=PS0JBTOx91C-z1Tb4Ky4NOnQeRosuW-7i1GIDUj088o",
            "heading": "the kanban board",
            "subheading": "you'll absolutely loveyou'll absolutely loveyou'll absolutely loveyou'll absolutely loveyou'll absolutely loveyou'll absolutely love",
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?w=200&h=200&white=true",
            "cta_text": "LEARN MORE",
            "website_url": "dolze.ai/download",
            "theme_color": "#44EC9D",
        }
    elif (
        templateName == "product_showcase"
        or templateName == "product_showcase_2"
    ):
        template_data = {
            "logo_url": "https://img.freepik.com/free-vector/bird-colorful-logo-gradient-vector_343694-1365.jpg?w=200&h=200&white=true",
            "product_image": "https://media.istockphoto.com/id/171384959/photo/executive-office-chair.jpg?s=612x612&w=0&k=20&c=5vRz91x_JdXHGrzWoDxtj7xEYvI35ls3pDfysHgd57M=",
            "product_name": "Strong chair",
            "product_price": "$52",
            "product_description": "made with highly refined wood made with highly refined wood ",
            "theme_color": "#44EC9D",
            "badge_text": "Bestseller",
        }
    elif templateName == "coming_soon_page":
        template_data = {
            "header_text": "We're Coming",
            "theme_color": "#44EC9D",
            "website_url": "dolze.ai/download",
            "contact_email": "contact@yourwebsite.com",
        }
    elif templateName == "coming_soon_post_2":
        template_data = {
            "text": "3 days left for our grand launch, get to experience our new product",
            "cta_text": "STAY TUNED",
            "website_url": "dolze.ai/download",
        }
    elif templateName == "hiring_post":
        template_data = {
            "theme_color": "#850aff",
            "heading": "dame un grrr",
            "subheading": "understood this? we are looking for you!",
            "job_title": "Social Media Lead",
            "website_url": "dolze.ai/download",
            "company_name": "Dolze",
            "cta_text": "apply now!",
        }
    elif templateName == "product_sale":
        template_data = {
            "product_name": "PROBIOTICS",
            "sale_text": "Flat 15% OFF",
            "product_description":"With Prebiotic Blend",
            "product_image":"https://t4.ftcdn.net/jpg/14/68/86/23/360_F_1468862392_uFV91fk0dgIrSUpRhYUqw7OcikgXpelA.webp",
            "bg_image": "https://dolze-templates-uat.s3.eu-north-1.amazonaws.com/uploads/a6fc48a9-8d1a-4dcf-87bc-93a4269c002c.png",
            "logo_url": "https://img.freepik.com/free-vector/gradient-s-letter-logo_343694-1365.jpg",
            "cta_text": "BUY NOW",
            "sale_end_text": "Ends 10th july at midnight",
            "sale_heading": "Flash Sale!"
        }
    elif templateName == "summer_sale_promotion":
        template_data = {
            "background_image_url": "https://img.freepik.com/free-photo/portrait-young-businesswoman-holding-eyeglasses-hand-against-gray-backdrop_23-2148029483.jpg?ga=GA1.1.1623013982.1744968336&semt=ais_hybrid&w=740",
            "theme_color": "#850aff",
            "brand_name": "Dolze AI",
            "sale_heading": "Summer Sale!",
            "sale_description": "Don't miss out on our biggest sale of the season. Shop now and refresh your business with our exclusive AI offerings.",
            "discount_text": "Up to 50% Off",
            "social_handle": "@dolze_ai",
            "contact_number": "+123-456-7890"
        }
    elif templateName == "product_showcase_3" :
        template_data = {
            "product_name": "Classic Scooter",
            "product_description": "Rent now for just $15.99/day.",
            "cta_text": "Book yours",
            "product_image": "https://media-public.canva.com/A6MI4/MAGbaAA6MI4/1/s3.png",
            "website_url": "dolze.ai/shop",
        }
    elif templateName == "quote_template":
        template_data = {
            "quote": "The only way to do your best work is to love what you do and dont do what you dont love.",
            "username": "@DolzeAi",
        }
    elif templateName == "product_service_minimal":
        template_data = {
            "text": "Minimalist product service",
            "website_url": "dolze.ai/shop",
            "product_image":"https://img.freepik.com/free-photo/furniture-background-clean-wall-wood_1253-666.jpg?t=st=1751691647~exp=1751695247~hmac=d5a191ec06d19843dcb271039a8e46a0374789e5a09714f0335e34139da25e43&w=1380",
        }
    elif templateName == "product_showcase_4":
        template_data = {
            "offer_text": "Get it only with Dolze",
            "product_image": "https://media-public.canva.com/A6MI4/MAGbaAA6MI4/1/s3.png",
            "website_url": "dolze.ai/shop",
            "theme_color": "#4A90E2",
        }
    elif templateName == "cafe_post":
        template_data = {
            "business_name": "The kind",
            "product_tagline": "Leading specialty brew",
            "social_handle": "@dolze_ai",
        }
    elif templateName == "coming_soon":
        template_data = {
            "background_image_url": "https://img.freepik.com/free-photo/close-up-meat-with-baked-potatoes-eggplant-tomato-pepper-decorated-with-pomegranate-wooden-bark_176474-2443.jpg?t=st=1751704275~exp=1751707875~hmac=1bb3b262f6a44e5898fcf5f70fb1be071981253d1b1db308ac972cf7f0e9e0ab&w=1380",
            "text": "COMING SOON",
            "website_url": "rumi.in",
            "business_name": "Rumi Restaurant",
            "logo_url": "https://img.freepik.com/free-vector/detailed-chef-logo-template_23-2148987940.jpg?t=st=1751704940~exp=1751708540~hmac=d327a7d9b9b689564d411580764d3308e521d60ea9b470ce9ed0c75b978d29d7&w=1380",
        }
    # Render the template with the data
    output_path = os.path.join("output", f"{templateName}.png")
    rendered_image = registry.render_template(
        templateName,
        template_data,
        output_path=output_path,
    )

    print(f"Template saved to {os.path.abspath(output_path)}")
    return rendered_image


def main():
    """Generate all example templates."""
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Generate all templates
        templates = [
            # "calendar_app_promo",
            # "testimonials_template",
            # "blog_post",
            # "education_info",
            # "education_info_2",
            # "calendar_app_promo",
            # "blog_post_2",
            # "education_info",
            # "product_promotion_2",
            # "promotional_banner",
            # "product_promotion",
            # "qa_template",
            # "quote_template",
            # "quote_template_2",
            # "product_showcase",
            # "testimonials_template_2",
            # "product_showcase_2",
            # "product_showcase_3",
            # "qa_template_2",
            # "qa_template",
            # "qa_template_3",
            # "education_info_2",
            # "coming_soon_page",
            # "coming_soon_post_2",
            # "hiring_post",
            # "product_sale",
            # "summer_sale_promotion",
            # "qa2",
            # "product_showcase_4",
            # "cafe_post",
            "coming_soon",
            # "product_service_minimal"
        ]
        for template in templates:
            generate_business_template(template)

        print("\nAll examples generated successfully!")
    except Exception as e:
        print(f"\nError generating examples: {str(e)}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
