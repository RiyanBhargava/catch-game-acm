# Create a simple ACM logo
import pygame

pygame.init()

# Create ACM logo
logo_surface = pygame.Surface((450, 450))
logo_surface.fill((30, 60, 120))  # ACM blue color

# Draw ACM text
font = pygame.font.Font(None, 120)
text = font.render("ACM", True, (255, 255, 255))
text_rect = text.get_rect(center=(225, 180))
logo_surface.blit(text, text_rect)

# Add subtitle
small_font = pygame.font.Font(None, 36)
subtitle = small_font.render("Association for", True, (255, 255, 255))
subtitle_rect = subtitle.get_rect(center=(225, 260))
logo_surface.blit(subtitle, subtitle_rect)

subtitle2 = small_font.render("Computing Machinery", True, (255, 255, 255))
subtitle2_rect = subtitle2.get_rect(center=(225, 290))
logo_surface.blit(subtitle2, subtitle2_rect)

# Add decorative elements
pygame.draw.rect(logo_surface, (255, 255, 255), (40, 40, 370, 370), 8)
pygame.draw.circle(logo_surface, (255, 255, 255), (225, 225), 180, 4)

# Save the logo
pygame.image.save(logo_surface, "acm.png")
print("ACM logo created successfully!")

pygame.quit()
