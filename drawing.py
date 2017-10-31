from PIL import Image, ImageDraw
import copy
def randrange(r):
    return random.randrange(int(r[0]), int(r[1]))
       
class Page_Element:
    def __init__(self, x, y, max_h, url, rectmode=None):
        self.x = x
        self.y = y
        self.max_h = max_h
        self.url = url
        self.rectmode = rectmode
        # load image and work out width and heights
        img_obj = Image.open(open(self.url, 'rb'))
        img_obj.thumbnail((10000, self.max_h), Image.ANTIALIAS)
        img_w, img_h = img_obj.size
        self.w = img_w
        self.h = img_h
    def draw(self, page):
        img_obj = Image.open(open(self.url, 'rb'))
        img_obj.thumbnail((10000, self.max_h), Image.ANTIALIAS)
        x_val = self.x
        y_val = self.y
        if self.rectmode == 'CENTER':
            x_val = self.x - self.w/2
            y_val = self.y - self.h/2
        page.paste(img_obj, (int(x_val), int(y_val)))

overflowing_element = None
class Page:
    def __init__(self, w=100, h=100, page_number=0, position='L', elements=[], bg_color="white"):
        self.w = w
        self.h = h
        self.page_number = page_number
        self.position = position
        self.elements = []
        self.bg_color = bg_color
        self.init_elements(elements)
    def init_elements(self, elements):
        new_elements = []
        global overflowing_element
        if len(elements) > 0:
            vertical_margin = self.h/3
            h_margin = 20
            for i in range(len(elements)):
                url = elements[i]
                if self.page_number == 0: # if birth page, render image in middle
                    x = self.w/2
                    y = vertical_margin
                    max_h = self.h - (vertical_margin * 2)
                else:
                    y = vertical_margin
                    max_h = self.h - (vertical_margin * 2)
                    
                    if len(new_elements) == 0: # look at last image on prev page if new page
                        prev_el = book[-1].elements[-1]
                        overflow_x = prev_el.x + prev_el.w + h_margin
                        overflow_image = Page_Element(x=overflow_x, y=y, max_h=max_h, url=url)
                        book[-1].elements.append(overflow_image)
                        x = prev_el.x + prev_el.w + h_margin - self.w
                        
                        if overflowing_element:
                            repeat_el = overflowing_element
                            repeat_el.x = repeat_el.x - self.w
                            new_elements.append(repeat_el)
                            overflowing_element = None
                    else:
                        prev_el = new_elements[-1]
                        x = prev_el.x + prev_el.w + h_margin

                new_element = Page_Element(x=x, y=y, max_h=max_h, url=url)           
                    
                if self.page_number == 0: # if birth page, move to center
                    new_element.x = new_element.x - new_element.w/2
                    
                # only add to page if it within page
                right = new_element.x + new_element.w
                left = new_element.x
             
                if (left < self.w and right > 0): 
                    new_elements.append(new_element)
                    if right > self.w: # if overflowing, store it
                        overflowing_element = copy.deepcopy(new_element)
        elif self.page_number == 27:
            if overflowing_element:
                repeat_el = overflowing_element
                repeat_el.x = repeat_el.x - self.w
                new_elements.append(repeat_el)
                overflowing_element = None
        self.elements = new_elements
                
    def draw(self, output_directory='one.png'):
        doc = Image.new('RGB', (self.w, self.h), self.bg_color)
        if len(self.elements) > 0:
            for i in self.elements:
                i.draw(page=doc)
        doc.save(output_directory, 'PNG')

book = []
def draw_book(plot):
    print('Drawing pages...')
    page_w = 2480
    page_h = 1748
                
    # Create cover
    cover = Page(w=page_w, h=page_h, page_number='C', position='R', bg_color="black")
    book.append(cover)
    # Create inside cover
    inside_cover = Page(w=page_w, h=page_h, page_number='IC', position='L')
    book.append(inside_cover)       
    # Collage pages
    for e in plot.events:
        position = 'R' if e.index % 2 == 0 else 'L'
        elements = e.images.copy()           
        collage_page = Page(w=page_w, h=page_h, page_number=e.index, position=position, elements=elements)
        book.append(collage_page)
    # Create inside back cover
    back_inside_cover = Page(w=page_w, h=page_h, page_number='BIC', position='R')
    book.append(back_inside_cover)  
    # Create back cover
    back_cover = Page(w=page_w, h=page_h, page_number='BC', position='L', bg_color="black")
    book.append(back_cover)
    return book
