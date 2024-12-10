from typing import Callable

from .. import AbstractMiddleware, Context

from PIL import Image


ImageType = Image.Image


class ScaleMiddleware(AbstractMiddleware):
    def next(
        self, next_: Callable[[Context], ImageType | None], context: Context
    ) -> ImageType | None:
        img = next_(context)
        if img:
            if (img.width, img.height) == (context.w, context.h):
                return img
            assert (img.width, img.height) < (context.w, context.h), \
                'scaling down is not allowed'
            try:
                return img.resize(
                    (context.w, context.h),
                    resample=Image.Resampling.NEAREST
                )
            finally:
                img.close()
