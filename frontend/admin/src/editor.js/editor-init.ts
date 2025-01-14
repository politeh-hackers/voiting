// editor-init.ts
import EditorJS, { LogLevels } from '@editorjs/editorjs';
import HeaderTool from '@editorjs/header';
import EmbedTool from '@editorjs/embed';
import ImageTool from '@editorjs/image';
import QuoteTool from '@editorjs/quote';
import GalleryTool from './tools/gallery';
import Table from '@editorjs/table';
import MapTool from './tools/map';
import CardTool, { CardToolData, CardType } from './tools/card';
import JSCookie from '../common/utils/cookie';
import { getToken, isAuthenticated } from '../utils/auth';

export const initEditor = (element: HTMLElement, data: any = null) => {
  let previousData: any = { blocks: [] };
  const deleteImage = (fileUrl: string) => {const imageName = fileUrl.split('/').pop(); // например, если fileUrl = 'http://localhost:8000/uploads/myimage.jpg', то imageName будет 'myimage.jpg'
  const token = getToken()
    return fetch(`http://127.0.0.1:8000/admin/image/${imageName}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `${token}`
      },
      body: JSON.stringify({ file_url: fileUrl })
    }).then((response) => {
      if (!response.ok) {
        alert('Ошибка при удалении изображения. Свяжитесь с администратором.');
      }
    });
  };
  const uploadImage = (image: File) => {
    const formData = new FormData();
    formData.append('image', image);
    formData.append('csrfmiddlewaretoken', JSCookie.get('csrftoken')!);

    return fetch('http://127.0.0.1:8000/admin/image', {
        method: 'post',
        body: formData
    }).then((response) => {
        if (!response.ok) {
            if (response.status == 400) {
                alert('Картинка слишком большая, уменьшите картинку и повторите попытку')
            } else if (response.status == 403) {
                alert('Отказано в доступе при загрузке картинок. Свяжитесь с администратором')
            }
            return null
        } else {
            return response.json();
        }
    }).then((data) => {
        if (data) {
            return {
                success: 1,
                file: data
            };
        } else {
            return {
                success: 0,
                file: null
            }
        }
    })
};


  const editor = new EditorJS({
    holder: element,
    logLevel: 'ERROR' as LogLevels,
    tools: {
      header: {
        class: HeaderTool,
        config: {
          levels: [2, 3],
          defaultLevel: 2
        }
      },
      quote: {
        class: QuoteTool,
        config: {
          quotePlaceholder: 'Введите цитату',
          captionPlaceholder: 'Введите подпись'
        }
      },
      embed: {
        class: EmbedTool,
        config: {
          services: {
            youtube: true,
            okru: {
              regex: /https?:\/\/ok\.ru\/video\/(\d+)/,
              embedUrl: 'https://ok.ru/videoembed/<%= remote_id %>',
              html: '<iframe src="{0}" height="300" scrolling="no" frameborder="no" allowtransparency="true" allowfullscreen="true" style="width: 100%; height: 300px;"></iframe>',
              height: 300,
              width: 600,
              id: (groups) => groups.join('/embed/')
            }
          }
        }
      },
      image: {
        class: ImageTool,
        config: {
          endpoints: {
            byFile: 'http://localhost:8000/admin/media'
          },
          uploader: {
            uploadByFile: uploadImage
          },
          onRemove: (data) => {
            if (data.file && data.file.url) {
              deleteImage(data.file.url);
            }
          }
        }
      },
      gallery: {
        class: GalleryTool,
        config: {
          uploader: {
            uploadByFile: uploadImage
          }
        }
      },
      card: {
        class: CardTool,
        config: {
          cardListUrl: (type: CardType, search: string) => `/admin/api/card-select/${type}?search=${search}`,
          cardUrl: (data: CardToolData) => `/admin/api/card/${data.type}/${data.id}`
        }
      },
      map: {
        class: MapTool,
        config: {
          center: [30.202880, 55.184220]
        }
      },
      table: {
        class: Table,
        config: {
          rows: 2,
          cols: 2,
        }
      },
    },
    data: data?.blocks ? data : { blocks: [] },
    onChange() {
      editor.save().then((currentData) => {
        const previousImages = previousData.blocks
          .filter((block) => block.type === 'image')
          .map((block) => block.data.file.url);
  
        const currentImages = currentData.blocks
          .filter((block) => block.type === 'image')
          .map((block) => block.data.file.url);
  
        const deletedImages = previousImages.filter(
          (url) => !currentImages.includes(url)
        );
  
        // Удаляем все удаленные изображения с сервера
        deletedImages.forEach((url) => deleteImage(url));
  
        // Обновляем предыдущее состояние
        previousData = currentData;
          });
    },
    
    i18n: {
        messages: {
            ui: {
                blockTunes: {
                    toggler: {
                        'Click to tune': 'Нажмите для настройки',
                        'or drag to move': 'или перетащите'
                    }
                },
                inlineToolbar: {
                    converter: {
                        'Convert to': 'Конвертировать'
                    }
                },
                toolbar: {
                    toolbox: {
                        'Add': 'Добавить'
                    }
                },
                popover: {
                    'Filter': 'Фильтр',
                    'Nothing found': 'Ничего не найдено'
                }
            },
            toolNames: {
                'Bold': 'Жирный',
                'Italic': 'Курсив',
                'Link': 'Ссылка',
                'Text': 'Параграф',
                'Heading': 'Заголовок',
                'Quote': 'Цитата',
                'Image': 'Фото',
                'Gallery': 'Галерея',
                'Card': 'Карточка',
                'Map': 'Карта',
                'Table': 'Таблица',
            },
            tools: {
                table: {
                    'Add row above': 'Добавить строку выше',
                    'Add row below': 'Добавить строку ниже',
                    'Delete row': 'Удалить строку',
                    'Delete column': 'Удалить столбец',
                    'Delete table': 'Удалить таблицу',
                    'Add column to left': 'Добавить колонку слева',
                    'Add column to right': 'Добавить колонку справа',
                    'Heading': 'Заголовок',
                    'With headings': 'С заголовками',
                    'Without headings': 'Без заголовков',
                },
                link: {
                    'Add a link': 'Добавить ссылку'
                },
                stub: {
                    'The block can not be displayed correctly.': 'Блок не может быть отображен'
                },
                header: {
                    'Heading 1': 'Заголовок H1',
                    'Heading 2': 'Заголовок H2',
                    'Heading 3': 'Заголовок H3',
                    'Heading 4': 'Заголовок H4',
                    'Heading 5': 'Заголовок H5',
                    'Heading 6': 'Заголовок H6'
                },
                gallery: {
                    'Add images': 'Добавить',
                    'Caption': 'Подпись'
                },
                image: {
                    'Select an Image': 'Выбрать',
                    'Caption': 'Подпись',
                    'With border': 'С рамкой',
                    'Stretch image': 'На всю ширину',
                    'With background': 'С фоном'
                },
                quote: {
                    'Enter a quote': 'Введите цитату',
                    'Enter a caption': 'Введите подпись'
                },
                card: {
                    'Select': 'Выбрать',
                    'Select card': 'Выбрать карточку',
                    'Search': 'Поиск'
                },
                map: {
                    'Caption': 'Подпись'
                }
            },
            blockTunes: {
                delete: {
                    'Delete': 'Удалить',
                    'Click to delete': 'Подтвердить удаление'
                },
                moveUp: {
                    'Move up': 'Переместить вверх'
                },
                moveDown: {
                    'Move down': 'Переместить вниз'
                }
            }
        }
    }
  });
  

  return editor;
};
