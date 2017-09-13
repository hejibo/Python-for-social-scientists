# Regions Of Interest
ROIS = {	'eyes':[325, 340, 330, 80],
		'nose':[415, 420, 140, 120],
		'mouth':[375, 540, 220, 100],
		'face':[295, 170, 400, 560],
		'not on face':[0, 0, 1024, 768]
		}
ROILIST = ['eyes', 'nose', 'mouth', 'face', 'not on face']

# create some images when called directly
if __name__ == "__main__":
	
	import os
	import pygame	
	pygame.init()
	pygame.font.init()
	
	fontfile = pygame.font.match_font('ubuntu')
	font = pygame.font.Font(fontfile, 24)
	
	filename = os.path.abspath(__file__).replace("ROIs_","").replace(".py", ".png")
	
	img = pygame.image.load(filename)
	imgsize = img.get_size()
	
	ROIimg = pygame.Surface(imgsize)
	ROIimg.fill((0,0,0))
	
	for ROIname in ['not on face', 'face', 'eyes', 'nose', 'mouth']:
		if ROIname == 'not on face':
			col = (100,100,100)
		elif ROIname == 'face':
			col = (150,150,150)
		else:
			col = (200,200,200)		
		ROIimg.fill(col, ROIS[ROIname])
		pygame.draw.rect(ROIimg, (0,0,0), ROIS[ROIname], 1)

	for ROIname in ROIS.keys():
		textsurf = font.render(ROIname, True, (0,0,0,255))
		blitpos = (	ROIS[ROIname][0] + 24,
				ROIS[ROIname][1] + 24)
		ROIimg.blit(textsurf, blitpos)
	
	pygame.image.save(ROIimg, filename.replace(".png", "_ROIs.png"))
	
	pygame.display.set_mode((1,1), pygame.NOFRAME|pygame.SRCALPHA)
	
	supimg = pygame.Surface(imgsize, pygame.SRCALPHA)
	img = img.convert()
	img.set_alpha(255)
	supimg.blit(img, (0,0))
	ROIimg.convert()
	ROIimg.set_alpha(200)
	supimg.blit(ROIimg, (0,0))
	pygame.image.save(supimg, filename.replace(".png", "_ROIs_superimposed.png"))
