import os
import re
import base64

def extract_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract Title (h1)
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
    title = ""
    if title_match:
        # Remove nested tags like <span>
        title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()
        # Clean up whitespace
        title = " ".join(title.split())
    
    # Extract Excerpt (first p tag after header usually, or just first p with text)
    # Looking at file, p is after h1
    excerpt_match = re.search(r'<p[^>]*>(.*?)</p>', content, re.DOTALL)
    excerpt = ""
    if excerpt_match:
        excerpt_clean = re.sub(r'<[^>]+>', '', excerpt_match.group(1)).strip()
        excerpt = " ".join(excerpt_clean.split())
        # Truncate if too long
        if len(excerpt) > 150:
            excerpt = excerpt[:147] + "..."
            
    # Extract Base64 Image
    image_match = re.search(r'data:image/png;base64,([^"\']+)', content)
    image_data = None
    if image_match:
        image_data = image_match.group(1).strip()
        # Fix padding
        missing_padding = len(image_data) % 4
        if missing_padding:
            image_data += '=' * (4 - missing_padding)
        
    return title, excerpt, image_data

def generate_card_html(title, excerpt, image_filename, link_filename, date="Oct 2023"):
    return f"""
            <a href="{link_filename}" class="blog-card">
                <div class="card-image-wrapper">
                    <img src="{image_filename}" alt="{title}" class="card-image">
                </div>
                <div class="card-content">
                    <div class="tags-container">
                        <span class="tag">Blog</span>
                        <span class="tag">Tech</span>
                    </div>
                    <h2 class="card-title">{title}</h2>
                    <p class="card-excerpt">
                        {excerpt}
                    </p>
                    <hr class="separator">
                    <div class="card-footer">
                        <span class="author-name">Janiru Hansaga</span>
                        <span class="divider">/</span>
                        <span>{date}</span>
                    </div>
                </div>
            </a>
    """

def main():
    base_dir = r"c:\Users\janir\OneDrive\Documents\MyPortfolio\janiruhansaga"
    thumbnails_dir = os.path.join(base_dir, "thumbnails")
    
    if not os.path.exists(thumbnails_dir):
        os.makedirs(thumbnails_dir)
        print(f"Created directory: {thumbnails_dir}")

    cards_html = ""
    
    # Process article-1.html to article-11.html
    for i in range(1, 12):
        filename = f"article-{i}.html"
        file_path = os.path.join(base_dir, filename)
        
        if not os.path.exists(file_path):
            print(f"Skipping {filename}, not found.")
            continue
            
        print(f"Processing {filename}...")
        title, excerpt, image_data = extract_content(file_path)
        
        image_filename = ""
        if image_data:
            image_filename = f"thumbnails/article-{i}.png"
            full_image_path = os.path.join(base_dir, image_filename)
            try:
                with open(full_image_path, "wb") as img_file:
                    img_file.write(base64.b64decode(image_data))
                print(f"Saved image to {image_filename}")
            except Exception as e:
                print(f"Failed to save image for {filename}: {e}")
                image_filename = "placeholder.png" # Fallback if save fails
        else:
            image_filename = "placeholder.png"

        cards_html += generate_card_html(title, excerpt, image_filename, filename)

    # Read post.html
    post_html_path = os.path.join(base_dir, "post.html")
    with open(post_html_path, 'r', encoding='utf-8') as f:
        post_content = f.read()

    # Construct the new grid content
    new_grid_content = f"""<div class="blog-grid" id="blogGrid">
{cards_html}
        </div>"""

    # Replace the existing blog-grid
    # Regex to find <div class="blog-grid" id="blogGrid"> ... </div>
    # We use a pattern that matches the opening tag, lazy content, and closing tag
    
    # Construct the new grid content
    new_grid_content = f"""<div class="blog-grid" id="blogGrid">
{cards_html}
        </div>"""

    # Robust replacement using prompts
    start_marker = '<div class="blog-grid" id="blogGrid">'
    end_marker = '<div class="pagination-container"'
    
    start_index = post_content.find(start_marker)
    end_index = post_content.find(end_marker)
    
    if start_index != -1 and end_index != -1:
        # Check if there is a closing div for the grid before the pagination
        # We need to preserve the whitespace before pagination if possible, but simplest is just to replace the block
        # The content to replace is from start_marker to end_marker
        # BUT we need to assume the blog-grid closes just before pagination-container.
        # Looking at file, there is </div>\n\n<div class="pagination...
        
        # Slicing: Keep everything before start_marker, add new content, keep everything from end_marker
        # We need to ensure we don't accidentally swallow the grid's closing div if it was separate, but we are reconstructing the grid wrapper in new_grid_content so we essentially replace the old wrapper + content.
        
        # However, we must be careful about what is between the last </a> and pagination.
        # Safest way: Find start, find end. 
        # Content between start and end should be replaced by new_grid_content + newlines.
        
        updated_content = post_content[:start_index] + new_grid_content + "\n\n        " + post_content[end_index:]
        print("Successfully replaced content using string slicing.")
    else:
        print("Markers not found, falling back to regex (risky) or failing.")
        updated_content = post_content # Do nothing if markers invalid
    
    with open(post_html_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("Successfully updated post.html")

if __name__ == "__main__":
    main()
