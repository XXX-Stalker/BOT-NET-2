import pyfiglet
import os
import time
import sys

class ASCIIArtGenerator:    
    def __init__(self):
        self.available_fonts = pyfiglet.FigletFont.getFonts()
        self.sample_text = "ASCII"
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def show_banner(self):
        banner = pyfiglet.figlet_format("ASCII ART", font="doom")
        print("=" * 60)
        print(banner)
        print(" " * 15 + "多功能艺术字生成器 v2.0")
        print("=" * 60)
    
    def show_available_fonts(self, num_samples=4):
        print("\n可用字体示例:")
        print("-" * 60)
        sample_fonts = [
            'standard', 'slant', 'block', 'bubble',
            'digital', 'doom', 'script', 'starwars'
        ][:num_samples]
        
        for font in sample_fonts:
            print(f"\n字体: {font}")
            print(pyfiglet.figlet_format(self.sample_text, font=font))
        
        print(f"\n共支持 {len(self.available_fonts)} 种字体")
        print("输入 'list' 查看完整字体列表")
    
    def list_all_fonts(self):
        print("\n完整字体列表:")
        print("-" * 60)
        for i, font in enumerate(self.available_fonts, 1):
            print(f"{i}. {font}")
            print(pyfiglet.figlet_format(self.sample_text, font=font))
        print("\n\n使用字体时请输入准确的字体名称")
    
    def generate_art(self, text, font="standard"):
        try:
            # 验证字体是否存在
            if font not in self.available_fonts:
                print(f"警告: 字体 '{font}' 不存在，使用默认字体")
                font = 'standard'
            
            # 生成ASCII艺术字
            ascii_art = pyfiglet.figlet_format(text, font=font)
            
            return ascii_art
        
        except Exception as e:
            print(f"生成错误: {e}")
            return None
    
    def save_to_file(self, artwork, filename="ascii_art.txt"):
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(artwork)
            print(f"\n已成功保存到 {filename}")
            return True
        except Exception as e:
            print(f"\n保存失败: {e}")
            return False
    
    def art_generator(self):
        self.clear_screen()
        self.show_banner()
        
        print("\n" + "=" * 30 + " 参数设置 " + "=" * 30)
        text = input("\n请输入要转换的文本: ").strip()
        if not text:
            print("文本不能为空！")
            time.sleep(1)
            return
        
        print("\n当前可用字体示例:")
        self.show_available_fonts()
        font = input("\n输入字体名称(留空使用默认，输入list查看全部): ").strip()
        
        if font.lower() == "list":
            self.list_all_fonts()
            font = input("\n请输入要使用的字体名称: ").strip()
        
        font = font or "standard"
        
        artwork = self.generate_art(text, font)
        if not artwork:
            print("生成失败，请重试")
            time.sleep(1)
            return
        
        self.clear_screen()
        print("\n" + "=" * 30 + " 生成结果 " + "=" * 30)
        print(artwork)
        print("=" * 72)
        
        save = input("\n是否保存到文件? (y/n): ").lower()
        if save == 'y':
            filename = input("输入文件名(留空使用ascii_art.txt): ").strip() or "ascii_art.txt"
            self.save_to_file(artwork, filename)
        
        input("\n按Enter键继续...")
    
    def main_menu(self):
        while True:
            self.clear_screen()
            self.show_banner()
            
            print("\n主菜单:")
            print("1. 生成艺术字")
            print("2. 查看字体示例")
            print("3. 查看完整字体列表")
            print("4. 退出程序")
            
            choice = input("\n请选择 (1-4): ").strip()
            
            if choice == "1":
                self.art_generator()
            elif choice == "2":
                self.clear_screen()
                self.show_available_fonts(num_samples=8)
                input("\n按Enter键返回主菜单...")
            elif choice == "3":
                self.clear_screen()
                self.list_all_fonts()
                input("\n按Enter键返回主菜单...")
            elif choice == "4":
                print("\n感谢使用，再见！")
                time.sleep(1)
                break

def main():
    try:
        generator = ASCIIArtGenerator()
        generator.main_menu()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        print(f"\n程序出错: {e}")
    finally:
        print("程序结束")
        sys.exit(0)

if __name__ == "__main__":
    main()