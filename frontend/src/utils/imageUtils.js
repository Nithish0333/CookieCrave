/**
 * Utility functions for handling product images
 */

/**
 * Gets the proper image URL for a product
 * @param {string} image - The image path, URL, or mealdb image URL
 * @param {string} fallback - Fallback image URL
 * @returns {string} The complete image URL
 */
export const getProductImageUrl = (image, fallback = null) => {
  if (!image) {
    return fallback || 'https://placehold.co/400x300/8B4513/FFFFFF?text=Cookie+Image';
  }
  
  // If it's a base64 image, return as is
  if (typeof image === 'string') {
    const trimmed = image.trim();
    // Handle base64 images from PostgreSQL
    if (trimmed.startsWith('data:image/')) {
      return trimmed;
    }
    // If it's already a full URL (http/https), return as is
    if (/^https?:\/\//i.test(trimmed)) {
      return trimmed;
    }
  }

  const backendUrl = 'http://127.0.0.1:8000';

  let imagePath = (typeof image === 'string' ? image.trim() : '');
  if (!imagePath) {
    return fallback || 'https://placehold.co/400x300/8B4513/FFFFFF?text=Cookie+Image';
  }

  // Normalize relative image paths into Media URL format.
  if (!imagePath.startsWith('/')) {
    imagePath = `/${imagePath}`;
  }

  if (imagePath.startsWith('/product_images/')) {
    imagePath = `/media${imagePath}`;
  } else if (!imagePath.startsWith('/media/')) {
    imagePath = `/media${imagePath}`;
  }

  return `${backendUrl}${imagePath}`;
};

/**
 * Gets a placeholder image URL with custom text
 * @param {string} text - Text to display on placeholder
 * @param {string} width - Width of placeholder (default: 400)
 * @param {string} height - Height of placeholder (default: 300)
 * @returns {string} Placeholder image URL
 */
export const getPlaceholderImageUrl = (text = 'Cookie', width = 400, height = 300) => {
  const colors = {
    chocolate: '8B4513',
    vanilla: 'FFE4B5',
    oatmeal: 'D2691E',
    fudge: '654321',
    default: '8B4513'
  };
  
  // Choose color based on text content
  let colorKey = 'default';
  if (text.toLowerCase().includes('chocolate')) colorKey = 'chocolate';
  else if (text.toLowerCase().includes('vanilla')) colorKey = 'vanilla';
  else if (text.toLowerCase().includes('oatmeal')) colorKey = 'oatmeal';
  else if (text.toLowerCase().includes('fudge')) colorKey = 'fudge';
  
  const bgColor = colors[colorKey];
  const textColor = colorKey === 'vanilla' ? '333333' : 'FFFFFF';
  
  return `https://placehold.co/${width}x${height}/${bgColor}/${textColor}?text=${encodeURIComponent(text)}+Cookie`;
};

/**
 * Image component props for consistent styling
 * @param {Object} props - Component props
 * @returns {Object} Image props object
 */
export const getImageProps = (image, alt, fallbackText = 'Cookie') => {
  return {
    src: getProductImageUrl(image, getPlaceholderImageUrl(fallbackText)),
    alt: alt || fallbackText,
    style: {
      width: '100%',
      height: '100%',
      objectFit: 'cover'
    },
    onError: (e) => {
      e.target.onerror = null;
      e.target.src = getPlaceholderImageUrl(fallbackText);
    }
  };
};

/**
 * Small image props for thumbnails
 * @param {Object} props - Component props
 * @returns {Object} Image props object
 */
export const getThumbnailProps = (image, alt, fallbackText = 'Cookie', size = 40) => {
  return {
    src: getProductImageUrl(image, getPlaceholderImageUrl(fallbackText, size, size)),
    alt: alt || fallbackText,
    style: {
      width: `${size}px`,
      height: `${size}px`,
      borderRadius: '4px',
      objectFit: 'cover'
    },
    onError: (e) => {
      e.target.onerror = null;
      e.target.src = getPlaceholderImageUrl(fallbackText, size, size);
    }
  };
};
