from playsound import playsound # thư viện giúp phát âm thanh
from gtts import gTTS # thu vien dung de chuyển  văn bản thành giọng nói
import os # thư viện giúp tương tác hệ điều hành


def text_to_speech(text, language="vi"):

    tts = gTTS(text=text, lang=language, slow=False)
    tts.save(r"D:\code\phanMemDoc\docLen.mp3") # lưu file mp3

    if len(text) < 100:
        playsound(r"D:\code\phanMemDoc\docLen.mp3") # Phát âm thanh
    elif len(text) >= 100:
        os.startfile(r"D:\code\phanMemDoc\docLen.mp3")

text = (
r"""
Các mô hình trí tuệ nhân tạo (AI), đặc biệt là trong thị giác máy tính, dựa vào dữ liệu được gắn nhãn chất lượng cao để học các mẫu và biểu diễn thế giới thực để xây dựng các mô hình mạnh mẽ. Tuy nhiên, việc thu thập dữ liệu như vậy là một nhiệm vụ đầy thách thức trong thế giới thực. Cần phải có nhiều thời gian và công sức để tuyển chọn các tập dữ liệu chất lượng cao và thực tế là không thể xác định và tuyển chọn dữ liệu cho tất cả các lớp trong một miền.

Với kiến ​​trúc mới, kỹ thuật đào tạo được tối ưu hóa và cơ chế đánh giá mạnh mẽ, người thực hiện có thể giải quyết các vấn đề kinh doanh phức tạp và nâng cao độ tin cậy của hệ thống AI.

Nhập Zero-shot learning (ZSL). Zero-shot learning (ZSL) cho phép các mô hình học máy nhận dạng các đối tượng từ các lớp mà chúng chưa từng thấy trong quá trình đào tạo. Thay vì chỉ dựa vào các tập dữ liệu được gắn nhãn mở rộng, ZSL tận dụng thông tin bổ trợ như các mối quan hệ ngữ nghĩa hoặc các thuộc tính học được từ dữ liệu đào tạo để thu hẹp khoảng cách giữa các lớp đã biết và chưa biết. 

Với ZSL, cuộc đấu tranh để dán nhãn các tập dữ liệu mở rộng được giảm đáng kể và các mô hình ML không còn cần phải trải qua quá trình đào tạo tốn thời gian để xử lý dữ liệu chưa biết trước đó.

Trong bài đăng này, bạn sẽ đi sâu vào ý nghĩa của mô hình học zero-shot, khám phá kiến ​​trúc của nó, liệt kê các mô hình ZSL nổi bật và thảo luận về các ứng dụng phổ biến và các thách thức chính.

Zero-Shot Learning là gì?
Học không-shot là một kỹ thuật cho phép các mô hình được đào tạo trước dự đoán nhãn lớp của dữ liệu chưa biết trước đó, tức là các mẫu dữ liệu không có trong dữ liệu đào tạo . Ví dụ, một mô hình học sâu (DL) được đào tạo để phân loại sư tử và hổ có thể phân loại chính xác một con thỏ bằng cách sử dụng học không-shot mặc dù không tiếp xúc với thỏ trong quá trình đào tạo. Điều này đạt được bằng cách tận dụng các mối quan hệ ngữ nghĩa hoặc thuộc tính (như môi trường sống, loại da, màu sắc, v.v.) liên quan đến các lớp, thu hẹp khoảng cách giữa các danh mục đã biết và chưa biết.

Học tập không-shot đặc biệt có giá trị trong các lĩnh vực như thị giác máy tính (CV) và xử lý ngôn ngữ tự nhiên (NLP), nơi quyền truy cập vào các tập dữ liệu được gắn nhãn bị hạn chế. Các nhóm có thể chú thích các tập dữ liệu lớn bằng cách tận dụng các mô hình học tập không-shot, đòi hỏi nỗ lực tối thiểu từ các chuyên gia chuyên ngành để gắn nhãn dữ liệu cụ thể cho từng lĩnh vực. Ví dụ, ZSL có thể giúp tự động hóa chú thích hình ảnh y tế để chẩn đoán hiệu quả hoặc tìm hiểu các mẫu DNA phức tạp từ dữ liệu y tế chưa được gắn nhãn.

Điều quan trọng là phải phân biệt zero-shot learning với one-shot learning và few-shot learning. Trong one-shot learning, một mẫu có sẵn cho mỗi lớp chưa thấy. Trong few-shot learning, một số lượng nhỏ mẫu có sẵn cho mỗi lớp chưa thấy. Mô hình tìm hiểu thông tin về các lớp này từ dữ liệu hạn chế này và sử dụng nó để dự đoán nhãn cho các mẫu chưa thấy.

Segment Anything Model (SAM) được biết đến với khả năng khái quát hóa zero-shot mạnh mẽ. Tìm hiểu cách sử dụng SAM để tự động gắn nhãn dữ liệu trong Encord trong bài đăng trên blog này .
Các loại học tập Zero-Shot
Có một số kỹ thuật học zero-shot có thể giải quyết những thách thức cụ thể. Chúng ta hãy cùng phân tích bốn phương pháp ZSL phổ biến nhất.

Học Zero-Shot dựa trên thuộc tính
ZSL dựa trên thuộc tính liên quan đến việc đào tạo một mô hình phân loại bằng cách sử dụng các thuộc tính cụ thể của dữ liệu được gắn nhãn. Các thuộc tính đề cập đến các đặc điểm khác nhau trong dữ liệu được gắn nhãn, chẳng hạn như màu sắc, hình dạng, kích thước, v.v. Một mô hình ZSL có thể suy ra nhãn của các lớp mới bằng cách sử dụng các thuộc tính này nếu lớp mới đủ giống với các lớp thuộc tính trong dữ liệu đào tạo.

Học tập Zero-Shot dựa trên nhúng ngữ nghĩa
Nhúng ngữ nghĩa là các biểu diễn vectơ của các thuộc tính trong không gian ngữ nghĩa, tức là thông tin liên quan đến ý nghĩa của từ, n-gram và cụm từ trong văn bản hoặc hình dạng, màu sắc và kích thước trong hình ảnh. Ví dụ, nhúng hình ảnh hoặc từ là một vectơ có chiều cao, trong đó mỗi phần tử biểu diễn một thuộc tính cụ thể. Các phương pháp như Word2Vec , GloVe và BERT thường được sử dụng để tạo nhúng ngữ nghĩa cho dữ liệu văn bản. Các mô hình này tạo ra các vectơ có chiều cao, trong đó mỗi phần tử có thể biểu diễn một thuộc tính ngôn ngữ hoặc ngữ cảnh cụ thể.

Các mô hình học Zero-shot có thể học các nhúng ngữ nghĩa này từ dữ liệu được gắn nhãn và liên kết chúng với các lớp cụ thể trong quá trình đào tạo. Sau khi được đào tạo, các mô hình này có thể chiếu các lớp đã biết và chưa biết lên không gian nhúng này. Bằng cách đo độ tương đồng giữa các nhúng bằng các phép đo khoảng cách, mô hình có thể suy ra loại dữ liệu chưa biết.

Một số phương pháp ZSL dựa trên nhúng ngữ nghĩa đáng chú ý là Semantic AutoEncoder (SAE) , DeViSE và VGSE .

SAE liên quan đến một khuôn khổ mã hóa-giải mã phân loại các đối tượng chưa biết bằng cách tối ưu hóa hàm tái tạo bị hạn chế. 

Tương tự như vậy, DeViSE đào tạo một mô hình nhúng ngữ nghĩa trực quan sâu để phân loại hình ảnh chưa biết thông qua thông tin ngữ nghĩa dựa trên văn bản. 

VGSE tự động học nhúng ngữ nghĩa của các mảng hình ảnh, yêu cầu chú thích tối thiểu ở cấp độ con người và sử dụng mô-đun quan hệ lớp để tính toán điểm tương đồng giữa nhúng lớp đã biết và chưa biết để học không cần thực hiện cú đánh nào.

Học tập Zero-Shot tổng quát (GZSL)
GZSL mở rộng kỹ thuật học zero-shot truyền thống để mô phỏng khả năng nhận dạng của con người. Không giống như ZSL truyền thống, chỉ tập trung vào các lớp chưa biết, GZSL đào tạo các mô hình trên các lớp đã biết và chưa biết trong quá trình học có giám sát . Bạn đào tạo các mô hình GSZL bằng cách thiết lập mối quan hệ giữa các lớp đã biết và chưa biết, tức là chuyển kiến ​​thức từ các lớp đã biết sang các lớp chưa biết bằng cách sử dụng các thuộc tính ngữ nghĩa của chúng. Một kỹ thuật bổ sung cho cách tiếp cận này là thích ứng miền. 

Thích ứng miền là một kỹ thuật học chuyển giao hữu ích về mặt này. Nó cho phép các học viên AI tái sử dụng một mô hình được đào tạo trước cho một tập dữ liệu khác chứa dữ liệu chưa được gắn nhãn bằng cách chuyển thông tin ngữ nghĩa.

Các nhà nghiên cứu Pourpanah, Farhad và cộng sự đã trình bày một đánh giá toàn diện về các phương pháp GZSL. Họ phân loại GZSL thành hai loại dựa trên cách kiến ​​thức được chuyển giao và học từ các lớp đã biết sang các lớp chưa biết:

Các phương pháp dựa trên nhúng: Thường dựa trên cơ chế chú ý, bộ mã hóa tự động, đồ thị hoặc học hai chiều. Các phương pháp như vậy học các biểu diễn ngữ nghĩa cấp thấp hơn bắt nguồn từ các đặc điểm trực quan của các lớp đã biết trong tập huấn luyện và phân loại các mẫu chưa biết bằng cách đo độ tương đồng của chúng với các biểu diễn của các lớp đã biết.
Các phương pháp dựa trên sinh sản : Các kỹ thuật này thường bao gồm Mạng đối nghịch sinh sản (GAN) và Bộ mã hóa tự động biến thể (VAE). Chúng học các biểu diễn trực quan từ các tính năng lớp đã biết và nhúng từ từ các mô tả lớp đã biết và chưa biết để đào tạo một mô hình sinh sản có điều kiện nhằm tạo các mẫu đào tạo. Quy trình này đảm bảo tập đào tạo bao gồm các lớp đã biết và chưa biết, biến việc học không bắn thành một vấn đề học có giám sát.
GZSL cung cấp phương pháp toàn diện và thích ứng hơn để nhận dạng và phân loại dữ liệu trên nhiều lớp dữ liệu hơn thông qua các phương pháp này.

Học tập Zero-Shot đa phương thức
ZSL đa phương thức kết hợp thông tin từ nhiều phương thức dữ liệu, chẳng hạn như văn bản, hình ảnh, video và âm thanh, để dự đoán các lớp chưa biết. Ví dụ, bằng cách đào tạo một mô hình sử dụng hình ảnh và mô tả văn bản liên quan của chúng, một học viên ML có thể trích xuất các nhúng ngữ nghĩa và phân biệt các liên kết có giá trị. Mô hình có thể trích xuất các nhúng ngữ nghĩa và tìm hiểu các liên kết có giá trị từ dữ liệu này. Với khả năng zero-shot, mô hình này có thể khái quát hóa thành các tập dữ liệu chưa biết tương tự với hiệu suất dự đoán chính xác.

Kiến trúc cơ bản của Zero-Shot Learning
Hãy xem xét một mô hình phân loại hình ảnh ZSL. Về cơ bản, nó bao gồm các mô-đun nhúng ngữ nghĩa và trực quan và một thành phần học zero-shot tính toán sự giống nhau giữa hai nhúng.

blog_image_11009

Tổng quan về Kiến trúc Học tập Zero-shot Cơ bản

Mô -đun nhúng ngữ nghĩa chiếu thông tin dạng văn bản hoặc dựa trên thuộc tính, như tài liệu, biểu đồ kiến ​​thức hoặc mô tả hình ảnh, lên không gian vectơ nhiều chiều. 

Tương tự như vậy, mô-đun nhúng trực quan chuyển đổi dữ liệu trực quan thành các nhúng nắm bắt các thuộc tính cốt lõi của hình ảnh. Cả nhúng ngữ nghĩa và nhúng trực quan đều được chuyển đến mô-đun ZSL để tính toán mức độ tương đồng của chúng và tìm hiểu mối quan hệ giữa chúng.

Học tập Zero-shot diễn ra như thế nào?
Quá trình học tập bao gồm việc giảm thiểu hàm mất mát được điều chỉnh theo trọng số của mô hình trên các ví dụ đào tạo. Hàm mất mát bao gồm điểm tương đồng có được từ mô-đun ZSL. Sau khi được đào tạo, mô hình phân loại một so với phần còn lại sau đó có thể dự đoán nhãn của một hình ảnh chưa biết bằng cách gán cho nó lớp mô tả văn bản có điểm tương đồng cao nhất. Ví dụ, nếu nhúng hình ảnh gần với nhúng văn bản có nội dung "một con sư tử", mô hình sẽ phân loại hình ảnh là một con sư tử.

Các mô-đun nhúng ngữ nghĩa và trực quan là các mạng nơ-ron chiếu hình ảnh và văn bản lên không gian nhúng. Các mô-đun có thể là các mô hình học sâu riêng biệt được đào tạo trên thông tin phụ trợ, như ImageNet . Đầu ra từ các mô hình này được đưa vào mô-đun ZSL và được đào tạo riêng biệt bằng cách giảm thiểu hàm mất mát độc lập. Ngoài ra, các mô-đun này có thể được đào tạo song song, như minh họa bên dưới.

blog_image_13126

Đào tạo chung các mô-đun ZSL

Một trình trích xuất tính năng được đào tạo trước sẽ chuyển đổi hình ảnh con mèo trong hình minh họa ở trên thành một vectơ N chiều. Vectơ này biểu diễn các tính năng trực quan của hình ảnh được đưa vào mạng nơ-ron. Đầu ra của mạng nơ-ron là một vectơ tính năng chiều thấp hơn. Sau đó, mô hình sẽ so sánh vectơ tính năng chiều thấp hơn này với vectơ thuộc tính lớp đã biết và sử dụng truyền ngược để giảm thiểu tổn thất (sự khác biệt giữa cả hai vectơ).

Tóm lại, khi bạn có được hình ảnh của một lớp mới, chưa biết (không phải là một phần của dữ liệu đào tạo), bạn sẽ:

Trích xuất các tính năng bằng trình trích xuất tính năng.
Chiếu các đặc điểm này vào không gian ngữ nghĩa bằng cách sử dụng mạng chiếu.
Tìm vectơ thuộc tính gần nhất trong không gian ngữ nghĩa để xác định lớp của hình ảnh.
Phương pháp sinh sản gần đây
Phương pháp học zero-shot truyền thống vẫn còn hạn chế vì chức năng chiếu của các mô-đun ngữ nghĩa và trực quan chỉ học cách ánh xạ các lớp đã biết vào không gian nhúng.

Không rõ thuật toán học tập sẽ hoạt động tốt như thế nào trên các lớp chưa biết và có khả năng là phép chiếu dữ liệu như vậy là không chính xác. Và đó là nơi GZSL đóng vai trò quan trọng bằng cách kết hợp dữ liệu đã biết và chưa biết làm tập huấn luyện.

Tuy nhiên, các phương pháp học tập khác với các phương pháp được mô tả ở trên. Mạng đối nghịch tạo sinh (GAN) và bộ mã hóa tự động biến thiên (VAE) là các kỹ thuật nổi bật trong lĩnh vực này.

Tổng quan ngắn gọn về Mạng đối nghịch tạo sinh (GAN) trong Học tập không cần bắn
GAN bao gồm một bộ phân biệt và một mạng lưới tạo. Mục tiêu của bộ tạo là tạo ra các điểm dữ liệu giả và bộ phân biệt học cách xác định xem các điểm dữ liệu là thật hay giả.

Các chuyên gia AI sử dụng khái niệm này để xử lý việc học zero-shot như một vấn đề dữ liệu bị thiếu. Hình minh họa bên dưới cho thấy kiến ​​trúc GAN điển hình cho ZSL.

blog_image_15368

Học Zero-Shot với GAN

Cơ chế hoạt động của kiến ​​trúc này như sau:

Trình trích xuất tính năng chuyển đổi hình ảnh thành một vectơ N chiều. 
Một vectơ thuộc tính tương ứng được sử dụng để đào tạo trước mạng máy phát. 
Đầu ra của mạng máy phát điện là một vectơ tổng hợp N chiều. 
Sau đó, bộ phân biệt sẽ so sánh hai vectơ để xem vectơ nào là giả.
Sau đó, bạn có thể đưa các nhúng ngữ nghĩa hoặc vectơ thuộc tính của các lớp không xác định vào trình tạo để tổng hợp các vectơ đặc trưng giả với các nhãn lớp có liên quan. Cùng với các vectơ đặc trưng thực tế, bạn có thể đào tạo mạng nơ-ron để phân loại các danh mục nhúng đã biết và chưa biết để đạt được độ chính xác của mô hình tốt hơn .

Tổng quan ngắn gọn về bộ mã hóa tự động biến thiên (VAE) trong học tập Zero-Shot
VAE, như tên gọi của nó, bao gồm các bộ mã hóa chuyển đổi phân phối dữ liệu đa chiều thành phân phối tiềm ẩn, tức là biểu diễn dữ liệu nhỏ gọn và đa chiều, giữ nguyên mọi thuộc tính quan trọng. Bạn có thể sử dụng phân phối tiềm ẩn để lấy mẫu các điểm dữ liệu ngẫu nhiên. Sau đó, bạn có thể đưa các điểm này vào mạng giải mã, mạng này sẽ ánh xạ chúng trở lại không gian dữ liệu gốc.

blog_image_17004

Kiến trúc VAE cơ bản

Giống như GAN, bạn có thể sử dụng VAE cho GZSL đa phương thức. Bạn có thể đào tạo mạng mã hóa để tạo phân phối trong không gian tiềm ẩn bằng cách sử dụng một tập hợp các lớp đã biết làm dữ liệu đào tạo, với nhúng ngữ nghĩa cho mỗi lớp.

Mạng giải mã có thể lấy mẫu một điểm ngẫu nhiên từ phân phối tiềm ẩn và chiếu nó lên không gian dữ liệu. Sự khác biệt giữa các lớp được tái tạo và lớp thực tế là lỗi học tập trong quá trình đào tạo bộ giải mã.

Sau khi được đào tạo, bạn đưa các nhúng ngữ nghĩa của các lớp không xác định vào mạng giải mã để tạo các mẫu có nhãn tương ứng. Bạn có thể đào tạo mạng phân loại cho nhiệm vụ phân loại cuối cùng bằng cách sử dụng dữ liệu đã tạo và dữ liệu thực tế.

Đánh giá các mô hình Zero-Shot Learning (ZSL)
Các học viên sử dụng một số số liệu đánh giá để xác định hiệu suất của các mô hình học tập zero-shot trong các tình huống thực tế. Các phương pháp phổ biến bao gồm:

Độ chính xác Top-K: Chỉ số này đánh giá xem lớp thực tế có khớp với các lớp dự đoán với xác suất top-k hay không. Ví dụ, xác suất lớp có thể là 0,1, 0,2 và 0,15 đối với bài toán phân loại ba lớp. Với độ chính xác top-1, mô hình hoạt động tốt nếu lớp dự đoán có xác suất cao nhất (0,2) khớp với lớp thực tế. Với độ chính xác top-2, mô hình hoạt động tốt nếu lớp thực tế khớp với bất kỳ lớp nào trong số các lớp dự đoán với điểm xác suất top-2 là 0,2 và 0,15.
Harmonic Mean: Bạn có thể tính toán harmonic mean—số giá trị chia cho nghịch đảo của trung bình số học—từ các giá trị độ chính xác top-1 và top-5 để có kết quả cân bằng hơn. Nó giúp đánh giá hiệu suất mô hình trung bình bằng cách kết hợp độ chính xác top-1 và top-5.
Diện tích dưới đường cong (AUC): AUC đo diện tích dưới đường cong đặc tính hoạt động của máy thu (ROC) , tức là một biểu đồ cho thấy sự đánh đổi giữa tỷ lệ dương tính thực (TPR) hoặc thu hồi so với tỷ lệ dương tính giả (FPR) của một bộ phân loại. Bạn có thể đo hiệu suất phân loại tổng thể của mô hình ZSL dựa trên số liệu này.
Độ chính xác trung bình trung bình (mAP): Số liệu mAP được sử dụng đặc biệt để đo độ chính xác của các tác vụ phát hiện đối tượng. Nó dựa trên việc đo độ chính xác và độ thu hồi cho mọi lớp nhất định ở nhiều mức ngưỡng tin cậy khác nhau. Phương pháp này giúp đo hiệu suất cho các tác vụ yêu cầu nhận dạng nhiều đối tượng trong một hình ảnh duy nhất. Nó cũng cho phép bạn xếp hạng điểm độ chính xác trung bình cho các ngưỡng khác nhau và xem ngưỡng nào mang lại kết quả tốt nhất.
Các mô hình Zero-Shot Learning (ZSL) phổ biến
Danh sách sau đây đề cập đến một số mô hình học tập zero-shot phổ biến được ứng dụng rộng rãi trong ngành.

Đào tạo trước hình ảnh ngôn ngữ tương phản (CLIP)
Được OpenAI giới thiệu vào năm 2021, CLIP sử dụng kiến ​​trúc mã hóa-giải mã để học zero-shot đa phương thức. Hình minh họa bên dưới giải thích cách CLIP hoạt động.

blog_image_21049

Kiến trúc CLIP
Tổng quan

Nó nhập các đoạn văn bản vào bộ mã hóa văn bản và hình ảnh vào bộ mã hóa hình ảnh. Nó đào tạo các bộ mã hóa để dự đoán đúng lớp bằng cách khớp hình ảnh với các mô tả văn bản phù hợp.

Bạn có thể sử dụng một tập dữ liệu văn bản của nhãn lớp làm chú thích và đưa chúng vào bộ mã hóa văn bản được đào tạo trước. Họ có thể nhập một hình ảnh chưa thấy vào bộ giải mã hình ảnh. Lớp được dự đoán sẽ thuộc về chú thích văn bản mà hình ảnh có điểm ghép nối cao nhất.

Bạn có muốn tìm hiểu cách đánh giá các mô hình dựa trên CLIP không? Hãy xem các bài đăng trên blog chi tiết của chúng tôi: Phần 1: Đánh giá các mô hình nền tảng (CLIP) bằng Encord Active và Phần 2: Đánh giá các mô hình nền tảng (CLIP) bằng Encord Active
Biểu diễn mã hóa song hướng từ máy biến áp (BERT)
BERT là một mô hình ngôn ngữ lớn theo trình tự-trình tự phổ biến sử dụng khuôn khổ mã hóa-giải mã dựa trên bộ biến đổi . Không giống như các mô hình tuần tự truyền thống có thể đọc các từ theo một hướng, bộ biến đổi sử dụng cơ chế tự chú ý để xử lý các câu theo cả hai hướng, cho phép hiểu sâu hơn về ngữ cảnh của trình tự. 

Trong quá trình đào tạo, mô hình học cách dự đoán một từ bị che giấu hoặc ẩn trong một câu nhất định. Nó cũng học cách xác định xem hai câu có được kết nối hay riêng biệt hay không. Thông thường, BERT được sử dụng như một mô hình được đào tạo trước để tinh chỉnh nó cho nhiều tác vụ NLP hạ lưu khác nhau, chẳng hạn như trả lời câu hỏi và suy luận ngôn ngữ tự nhiên.

blog_image_23540

Kiến trúc tiền đào tạo và tinh chỉnh BERT

Mặc dù BERT ban đầu không được thiết kế với khả năng zero-shot, nhưng các học viên đã phát triển nhiều biến thể BERT có khả năng thực hiện học zero-shot. Các mô hình như ZeroBERTo , ZS-BERT và BERT-Sort có thể thực hiện nhiều tác vụ NLP trên dữ liệu chưa biết.

Bộ chuyển đổi văn bản sang văn bản (T5)
T5 tương tự như BERT, sử dụng khung mã hóa-giải mã dựa trên bộ biến đổi . Mô hình chuyển đổi tất cả các tác vụ ngôn ngữ thành định dạng văn bản sang văn bản, tức là lấy văn bản làm đầu vào và tạo văn bản làm đầu ra. Cách tiếp cận này cho phép các học viên áp dụng cùng một mô hình, tham số và quy trình giải mã cho tất cả các tác vụ ngôn ngữ. Do đó, mô hình mang lại hiệu suất tốt cho một số tác vụ NLP, chẳng hạn như tóm tắt, phân loại, trả lời câu hỏi, dịch và xếp hạng.

blog_image_25134

Tổng quan về Kiến trúc T5

Vì T5 có thể được áp dụng cho nhiều tác vụ khác nhau, các nhà nghiên cứu đã điều chỉnh nó để đạt được hiệu suất tốt cho việc học zero-shot. Ví dụ, RankT5 là một mô hình xếp hạng văn bản hoạt động tốt trên các tập dữ liệu ngoài miền . Một biến thể khác của mô hình T5, Flan T5 , tổng quát hóa tốt cho các tác vụ chưa được biết đến.

Những thách thức của mô hình Zero-Shot Learning (ZSL)
Mặc dù việc học không cần bắn mang lại những lợi ích đáng kể, nhưng nó vẫn đặt ra một số thách thức mà các nhà nghiên cứu và thực hành AI cần giải quyết. Bao gồm:

Sự trung thành
Vấn đề hubness xảy ra do bản chất chiều cao của việc học zero-shot. Các mô hình ZSL chiếu dữ liệu lên không gian ngữ nghĩa chiều cao và phân loại các điểm không nhìn thấy bằng cách sử dụng tìm kiếm lân cận gần nhất (NN).

Tuy nhiên, không gian ngữ nghĩa thường có thể chứa "trung tâm" nơi các điểm dữ liệu cụ thể gần với các mẫu khác. Sơ đồ bên dưới minh họa vấn đề trong không gian hai chiều.

blog_image_26658

Vấn đề Hubness

Bảng (a) trong sơ đồ cho thấy các điểm dữ liệu tạo thành một trung tâm xung quanh lớp 2. Điều này có nghĩa là mô hình sẽ phân loại sai hầu hết các lớp chưa thấy là lớp 2 vì nhúng của chúng gần nhất với lớp 2. Vấn đề trở nên nghiêm trọng hơn ở các chiều cao hơn.

Bảng (b) cho thấy tình huống khi không có tính trung tâm và dự đoán lớp có phân phối đều.

Mất mát ngữ nghĩa
Khi chiếu các lớp đã thấy lên không gian ngữ nghĩa, các mô hình học zero-shot có thể bỏ lỡ thông tin ngữ nghĩa quan trọng. Chúng có xu hướng tập trung vào ngữ nghĩa, điều này chỉ giúp chúng phân loại các lớp đã thấy. Ví dụ, một mô hình ZSL được đào tạo để phân loại ô tô và xe buýt có thể không dán nhãn đúng cho xe đạp vì nó không tính đến ô tô và xe buýt có bốn bánh. Đó là vì thuộc tính “ có bốn bánh ” không cần thiết khi phân loại xe buýt và ô tô.

Chuyển miền
Các mô hình học Zero-shot có thể bị ảnh hưởng bởi sự dịch chuyển miền khi phân phối tập huấn luyện khác đáng kể so với tập kiểm tra. Ví dụ, một mô hình ZSL được huấn luyện để phân loại mèo hoang có thể không phân loại được các loài côn trùng, vì các đặc điểm và thuộc tính cơ bản có thể thay đổi đáng kể.

Sự thiên vị
Sai lệch xảy ra khi các mô hình học zero-shot chỉ dự đoán các lớp thuộc về dữ liệu đã thấy. Các mô hình không thể dự đoán bất cứ điều gì nằm ngoài các lớp đã thấy. Sai lệch cố hữu này có thể cản trở khả năng dự đoán hoặc nhận dạng các lớp chưa thấy của mô hình.

Ứng dụng của Zero-Shot Learning (ZSL)
Kỹ thuật học không cần bắn được áp dụng cho một số tác vụ AI, đặc biệt là tác vụ thị giác máy tính, chẳng hạn như:

Tìm kiếm hình ảnh: Công cụ tìm kiếm có thể sử dụng mô hình ZSL để tìm và truy xuất hình ảnh có liên quan đến truy vấn tìm kiếm của người dùng.
Chú thích hình ảnh: Các mô hình ZSL có khả năng gắn nhãn theo thời gian thực rất tốt, giúp người gắn nhãn chú thích hình ảnh phức tạp ngay lập tức bằng cách giảm bớt công sức thủ công cần thiết cho việc gắn nhãn hình ảnh.
Phân đoạn ngữ nghĩa: Việc gắn nhãn các phân đoạn hình ảnh cụ thể rất tốn công. Các mô hình ZSL giúp xác định các phân đoạn có liên quan và gán cho chúng các lớp phù hợp.
Phát hiện vật thể: Các mô hình ZSL có thể giúp xây dựng hệ thống dẫn đường hiệu quả cho xe tự hành vì chúng có thể phát hiện và phân loại nhiều vật thể vô hình theo thời gian thực, đảm bảo hoạt động tự hành an toàn hơn và phản ứng nhanh hơn.
Đọc về phân đoạn ngữ nghĩa trong bài viết chi tiết này, Giới thiệu về phân đoạn ngữ nghĩa .
Zero-Shot Learning (ZSL): Những điểm chính cần ghi nhớ
Học tập không bắn là một lĩnh vực nghiên cứu tích cực vì nó hứa hẹn đáng kể cho tương lai của AI. Dưới đây là một số điểm chính cần nhớ về ZSL.

Hiệu quả phân loại: ZSL cho phép các chuyên gia AI xác định ngay lập tức các lớp chưa thấy, giải phóng họ khỏi việc dán nhãn tập dữ liệu theo cách thủ công.
Nhúng ở cốt lõi: Các mô hình ZSL cơ bản sử dụng nhúng ngữ nghĩa và trực quan để phân loại các điểm dữ liệu chưa biết.
Tiến bộ về mặt sinh sản : Các phương pháp sinh sản hiện đại cho phép ZSL khắc phục các vấn đề liên quan đến nhúng chiều cao.
Vấn đề về độ trung tâm: Thách thức quan trọng nhất trong ZSL là vấn đề độ trung tâm.
GZSL đa phương thức có thể giúp giảm thiểu nhiều vấn đề bằng cách sử dụng dữ liệu hữu hình và vô hình để đào tạo.



"""
)
text_to_speech(text)
