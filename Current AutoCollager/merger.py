from PIL import Image, ImageOps
import math
import os
from pathlib import Path


class Merger:

    def __init__(self, final_img_size, is_width_priority=True):

        self.default_save_path = str(os.path.join(Path.home(), "Downloads"))

        self.final_size = final_img_size
        self.final_is_width_priority = is_width_priority
        
    def setFinalSize(self, size):
        self.final_size = size
        print("final size is now:",  self.final_size)

    def openImages(self, img_filename_list, exif_fix=True):
        obj_list = []
        for img_filename in img_filename_list:
            img = Image.open(img_filename)
            if exif_fix:
                img = ImageOps.exif_transpose(img) # re-orientate images according to EXIF
            obj_list.append(img)

        return obj_list

    def closeImages(self, img_obj_list):
        for ImgObj in img_obj_list:
            ImgObj.close()


    def getLargestDimension(self, img_obj_list, dimIsWidth=True):
        max_dim = 0
        for Img in img_obj_list:
            dimension = Img.size[not dimIsWidth]
            if dimension > max_dim:
                max_dim = dimension
        return max_dim


    def getRowHeights(self, img_obj_list, rows, cols):
        num_images = len(img_obj_list)
        row_heights = []
        for r in range(rows):
            start_index = r * cols
            end_index = (r + 1) * cols
            print(f"indices: {start_index}, {end_index}")
            if end_index > num_images:
                print(f"end_index is larger than num_images, {num_images}")
                end_index = num_images

            curr_row = img_obj_list[start_index:end_index]
            print(f"num obj in curr row is {len(curr_row)}, curr_row: {curr_row}")
            row_heights.append(self.getLargestDimension(curr_row, False))

        return row_heights


    def _calcWidth(self, num_cols, max_width, border_thickness, outer_border_thickness):
        return (num_cols * max_width) + ((num_cols-1) * border_thickness) + (2 * outer_border_thickness)


    def _calcHeight(self, row_heights, border_thickness, outer_border_thickness):
        return sum(row_heights) + ((len(row_heights)-1) * border_thickness) + (2 * outer_border_thickness)

    
    def scaleImageToWidth(self, Img, new_width):
        scaled_height = int(new_width * (Img.size[1] / Img.size[0]))
        NewImg = Img.resize((new_width, scaled_height), Image.Resampling.LANCZOS)
        return NewImg

    def scaleImagesToWidth(self, img_obj_list, new_width):
        new_img_obj_list = []
        for Img in img_obj_list:          
            new_img_obj_list.append(self.scaleImageToWidth(Img, new_width))
        return new_img_obj_list


    def scaleImageToHeight(self, Img, new_height):
        scaled_width = int(new_height * (Img.size[0] / Img.size[1]))
        NewImg = Img.resize((scaled_width, new_height), Image.Resampling.LANCZOS)
        return NewImg


    def scaleImagesToHeight(self, img_obj_list, new_height):
        new_img_obj_list = []
        for Img in img_obj_list:          
            new_img_obj_list.append(self.scaleImageToHeight(Img, new_height))
        return new_img_obj_list


    def determineLayout(self, num_images):
        if num_images == 1:
            rows = 1
            cols = 1
        
        elif num_images <= 3:
            rows = 1
            cols = num_images

        elif num_images > 3:
            sqrt_num_img = math.sqrt(num_images)
            if sqrt_num_img.is_integer():
                rows = int(sqrt_num_img)
                cols = int(sqrt_num_img)
            else:
                rows = math.isqrt(num_images)
                cols = num_images // rows

                if (rows * cols) != num_images: # left overs go to a new row
                    cols += 1
                    
        print(f"\tlayout: ({rows}, {cols})")
        return (rows, cols)


    def mergeImages(self, img_obj_list, layout, filename, border_color, border_thickness, outer_border_thickness):
        #variables
        num_images = len(img_obj_list)
        num_rows, num_cols = layout #self.determineLayout(num_images)


        #calculate final dimensions and make adjustments
        if self.final_is_width_priority:
            max_img_width = self.getLargestDimension(img_obj_list, True)
            total_width = self._calcWidth(num_cols, max_img_width, border_thickness, outer_border_thickness)

            print(f"\tmax_img_width: {max_img_width}, total_width: {total_width}")

            if total_width > self.final_size[0]: #solve for appriorate width
                max_img_width = int((self.final_size[0] - ((num_cols-1) * border_thickness) - (2 * outer_border_thickness)) / num_cols)
                total_width = self._calcWidth(num_cols, max_img_width, border_thickness, outer_border_thickness)
                
                print(f"\tTotal width too large, so recalc's are max_img_width: {max_img_width}, total_width: {total_width}")

            #rescale images
            img_obj_list = self.scaleImagesToWidth(img_obj_list, max_img_width)
            row_heights = self.getRowHeights(img_obj_list, num_rows, num_cols)
            total_height = self._calcHeight(row_heights, border_thickness, outer_border_thickness)

            print(f"row heights: {row_heights}, sum of heights: {sum(row_heights)}, total_height: {total_height}")

        else:
            row_heights = self.getRowHeights(img_obj_list, num_rows, num_cols)
            total_height = self._calcHeight(row_heights, border_thickness, outer_border_thickness)

            if total_height > self.final_size[1]: #computionally find good row heights
                print("\ttotal_height too large, {total_height} > {self.final_size[1]}, computationally finding better values for row heights...")
            
                factor = 0.95
                decrement = 0.05
                while (total_height > self.final_size[1]):
                    for i in range(len(row_heights)):
                        row_heights[i] = int(factor * row_heights[i])
                    total_height = self._calcHeight(row_heights, border_thickness, outer_border_thickness)
        
                    print(f"\t\tFor factor of image size, {factor}, total_height is {total_height}")
                    factor -= decrement            

                #rescale images
                for row in range(num_rows):
                    start_index = row * num_cols
                    end_index = (row + 1) * num_cols
                    if end_index > num_images:
                        end_index = num_images
                        print("\tend index is num_images")

                    print("\tindexes: ", start_index, end_index)
                    curr_row = img_obj_list[start_index:end_index]
                    curr_new_height = row_heights[row]
                    img_obj_list[start_index:end_index] = self.scaleImagesToHeight(curr_row, curr_new_height)

                _row_heights = self.getRowHeights(img_obj_list, num_rows, num_cols)
                if _row_heights != row_heights:
                    print(f"\tError: scaling images by height failed. Result, {_row_heights}, doesn't match target, {row_heights}")

                #find final image width due to scaling
                max_img_width = self.getLargestDimension(img_obj_list, True)
                total_width = self._calcWidth(num_cols, max_img_width, border_thickness, outer_border_thickness)
                

        print(f"\tfinal image size: ({total_width}, {total_height})")
        
        #actually make the image
        FinalImg = Image.new("RGBA", (total_width, total_height), border_color)
         
        
        
        y_pos = outer_border_thickness
        for row in range(num_rows):
            y_pos += (row > 0) * (row_heights[row-1] + border_thickness)
            for col in range(num_cols):
                i = row * num_cols + col
                x_pos = col * (max_img_width + border_thickness) + outer_border_thickness
                
                if i < num_images:
                    Img = img_obj_list[i]
                    centring_offset = int((max_img_width - Img.size[0]) / 2)
                    x_pos += centring_offset
                    
                    print(f"\trow: {row}")
                    print(f"\tcentring offset: {centring_offset}")
                    print(f"\tpos for image {i} of size {Img.size} is ({x_pos}, {y_pos})")

                    FinalImg.paste(Img, (x_pos, y_pos))

        FinalImg.save(filename)
