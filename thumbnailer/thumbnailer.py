from multiprocessing import Process, Queue


def _thumbnailer(queue):
    from PIL import Image
    import os

    while True:
        s = queue.get()
        try:
            img = Image.open(s)
            w, h = img.size
            if w <= 10000 and h <= 10000:
                img.thumbnail((256, 256))
                dr, f = os.path.split(s)
                img.save(os.path.join(dr, "thumbnail_" + f))
        except Exception as e:
            print(e)


class Thumbnailer:

    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def __init__(self):
        self.queue = Queue()
        self.p = Process(target=_thumbnailer, args=(self.queue,))
        self.p.daemon = True
        self.p.start()

    def make_thumbnail(self, image_path):
        self.queue.put_nowait(image_path)

